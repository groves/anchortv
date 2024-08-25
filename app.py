from starlette.applications import Starlette
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sheets import fetch_sheet_data
from datetime import datetime, date
from dataclasses import dataclass
from config import Config


@dataclass
class Exercise:
    name: str
    reps: str
    effort: str


@dataclass
class Week:
    days: list[list[Exercise]]
    start: date
    end: date


config = Config()
templates = Jinja2Templates(directory="templates")


def parse_date(month_day: str) -> date:
    now = datetime.now()

    # We don't have a year in the sheet, so we want the date that's closest to now.
    # Set it to the current year as a starting point.
    parsed = datetime.strptime(month_day, "%b %d").replace(year=now.year)

    days_apart = (parsed - now).days

    if days_apart > 180:
        # The parsed date is more than six months later than the current date if it's set to the
        # current year.
        # That means the date is actually in the previous year
        return parsed.replace(year=now.year - 1).date()
    elif days_apart < -180:
        # The parsed date is more than six months earlier than the current date if it's set to the
        # current year.
        # That means the date is actually in the next year
        return parsed.replace(year=now.year + 1).date()
    else:
        # It's within six months, so it's in the current year
        return parsed.date()


def load_block():
    CLASS_RANGE = "A1:D1000"
    # TODO pick between multiple classes based on the current time
    rows = fetch_sheet_data(config.classes[0].sheet, CLASS_RANGE)
    weeks = []
    for i, row in enumerate(rows):
        if not row:
            continue
        if row[0].upper().startswith("WEEK"):
            start, end = row[1].split(" -- ")
            weeks.append(Week([], parse_date(start), parse_date(end)))
        elif row[0].upper().startswith("DAY"):
            weeks[-1].days.append([])
        elif weeks:
            if row[1].upper() == "NA" or row[0].upper() == "MOVEMENT":
                continue
            name = row[0] if row[0] else rows[i - 1][0]
            if len(row) > 2:
                effort = row[2] if row[2] else row[3]
            else:
                effort = ""
            weeks[-1].days[-1].append(Exercise(name=name, reps=row[1], effort=effort))
    return weeks


def homepage(request):
    weeks = load_block()
    now = datetime.now().date()

    for i, week in enumerate(weeks):
        if week.start > now or week.end < now:
            continue
        # Show day 0 on monday or tuesday, day 1 on wednesday or thursday, and day 3 otherwise
        if now.weekday() <= 1:
            day = 0
        elif now.weekday() <= 3:
            day = 1
        else:
            day = 2
        return templates.TemplateResponse(
            request,
            "index.jinja",
            {"week": i + 1, "day": day + 1, "exercises": weeks[i].days[day]},
        )
    raise Exception("Couldn't find day")


app = Starlette(
    debug=True,
    routes=[
        Route("/", endpoint=homepage),
        Mount("/static", app=StaticFiles(directory="static", html=True), name="static"),
    ],
)
