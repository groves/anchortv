from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]


def fetch_sheet_data(spreadsheet_id, cells, sheet_index=0):
    creds = Credentials.from_service_account_file("google-creds.json", scopes=SCOPES)
    service = build("sheets", "v4", credentials=creds)

    sheet = service.spreadsheets()

    sheet_metadata = sheet.get(spreadsheetId=spreadsheet_id).execute()
    title = sheet_metadata["sheets"][sheet_index]["properties"]["title"]

    range = f"'{title}'!{cells}"

    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range).execute()
    return result.get("values", [])


if __name__ == "__main__":
    from config import Config

    rows = fetch_sheet_data(Config().classes[0].sheet, "A113:D118")
    for row in rows:
        print(row)
