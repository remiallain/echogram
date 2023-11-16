# Echogram

Effortless **Telegram channels monitoring** - Archiving messages from Telegram channels into daily ND-JSON files.

## Setup

1. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the project directory with the following variables:

   ```dotenv
   TG_API_ID=your_telegram_api_id
   TG_API_HASH=your_telegram_api_hash
   TG_DATA_DIR=/path/to/data/directory
   TG_CHANNELS=channel_username1,channel_username2,channel_username3
   TG_SESSION_ID=your_session_id
   LOGLEVEL=INFO
   ```

   Ensure you replace the placeholders with your actual values.

## Usage

Run the script using the following command:

```bash
python src/main.py
```

The script will authenticate your Telegram account, listen to the specified channels, and log incoming messages into newline-delimited JSON files in the designated data directory.

## Notes

- The script logs messages for the specified channels only.
- Each day's messages are stored in a separate `.ndjson` file.
- Ensure the specified channels exist and are accessible by the authenticated account.
