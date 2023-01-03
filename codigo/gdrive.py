from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def update_values(values):
    """
    Insere o parametro na planilha, segue abaixo exemplo de paramêtro.

    values = [
        ['10-11-13', 'Brasil'],
        ['10-11-14', 'Argentina']
    ]
    """
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # pylint: disable=maybe-no-member
    try:

        service = build('sheets', 'v4', credentials=creds)
        # The ID of the spreadsheet to update.
        spreadsheet_id = '1ene0rIqqgP5wDQJrLII2M5bhqfH21lHK7zyx0yJt7vc'  # TODO: Update placeholder value.
        # The A1 notation of the values to clear.
        range_name = 'A2:M'  # TODO: Update placeholder value.
        body = {'values': values}
        result = (
            service.spreadsheets()
            .values()
            .update(
                spreadsheetId=spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body,
            )
            .execute()
        )
        print(f"{result.get('updatedCells')} cells updated.")
        return result
    except HttpError as error:
        print(f'An error occurred: {error}')
        return error


def delete_values():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    credentials = Credentials.from_authorized_user_file('token.json', SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # The ID of the spreadsheet to update.
    spreadsheet_id = '1ene0rIqqgP5wDQJrLII2M5bhqfH21lHK7zyx0yJt7vc'  # TODO: Update placeholder value.
    # The A1 notation of the values to clear.
    range_ = 'A2:M'  # TODO: Update placeholder value.

    clear_values_request_body = {
        # TODO: Add desired entries to the request body.
    }

    request = (
        service.spreadsheets()
        .values()
        .clear(
            spreadsheetId=spreadsheet_id,
            range=range_,
            body=clear_values_request_body,
        )
    )
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    return response
