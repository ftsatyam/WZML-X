<p align="center">
   Heroku Supported Lite Version Of WZML-X
</p>

<p align="center">
   <img src="docs/HK-icon.svg" alt="HKML-X logo" width="160">
</p>

<h1 align="center">HKML-X</h1>

<p align="center">
   A powerful Telegram bot for downloading files/folders from MEGA, Torrents, AllDebrid, Direct Cloud Links, Google Drive, Telegram, yt-dlp & Upload Back to Telegram, Google Drive, 70+ Rclone-supported cloud storage platforms & Uphoster Platforms(GoFile, PixelDrain, Devuploads, Vikingfile, Buzzheavier).
</p>

<p align="center">
   <a href="https://t.me/HKML_X">
      <img src="https://img.shields.io/badge/Telegram-Community-26A5E4?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
   </a>
</p>

## Supported Platforms

<details>
<summary><strong>Download From</strong></summary>

- Telegram (Files/Links)
- Direct Download Links (DDL)
- Torrents, magnet links & Seedr links
- Google Drive and Rclone remotes
- MEGA (Files & Folder Links)
- Supported links through yt-dlp and AllDebrid
</details>

<details>
<summary><strong>Upload To</strong></summary>

- Telegram
- Google Drive
- Uphoster Platforms (GoFile, PixelDrain, Devuploads, Vikingfile, Buzzheavier)
- 70+ Rclone Supported Platforms
</details>

## Variables

<details>
<summary><strong>Click Here</strong></summary>

### Required Variables

- **`BOT_TOKEN`** - Telegram bot token from [@BotFather](https://t.me/BotFather)
- **`TELEGRAM_API`** - Telegram API ID from [my.telegram.org](https://my.telegram.org)
- **`TELEGRAM_HASH`** - Telegram API hash from [my.telegram.org](https://my.telegram.org)
- **`OWNER_ID`** - Your Telegram user ID
- **`DATABASE_URL`** - MongoDB URL for persistence and database-backed features.

### Optional Variables
- **`AUTHORIZED_CHATS`** - Comma-separated chat IDs allowed to use the bot
- **`SUDO_USERS`** - Telegram user IDs with elevated bot permissions
- **`CMD_SUFFIX`** - Suffix added to bot commands
- **`DEFAULT_UPLOAD`** - Default upload destination
- **`GDRIVE_ID`**, **`RCLONE_PATH`** - Google Drive and Rclone destination settings
- **`MEGA_EMAIL`**, **`MEGA_PASSWORD`** - Premium Mega account credentials for higher download limits
- **`SEEDR_EMAIL`**, **`SEEDR_PASSWORD`** - Seedr account credentials
- **`ALLDEBRID_API_KEY`** - AllDebrid API key
- **`DISABLE_*`** - Disable supported integrations or features
- **`*_LIMIT`** - Source and task size limits in GB; `0` means Unlimited for that setting
- **`QUEUE_ALL`**, **`QUEUE_DOWNLOAD`**, **`QUEUE_UPLOAD`** - Task queue limits
- **`WEB_PINCODE`** - Control PIN protection for the torrent-selection web interface
- **`UPSTREAM_REPO`**, **`UPSTREAM_BRANCH`** - Repository and branch for auto update.
- **`BASE_URL`**, **`TG_PROXY`**, **`USER_SESSION_STRING`** - Web, proxy, or user-session settings

For every supported option and its default, see [`config_sample.py`](config_sample.py).
</details>

## Deployment

</details>

<details>
  <summary><strong>Heroku CLI</strong></summary>

1. **Login to Heroku**
   ```bash
   heroku login
   ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/ImKrishana/HK-Deploy DP && cd DP
   ```

3. **Create `config.py` File**
   ```bash
   nano config.py
   ```

   Add the required variables:
   ```python
   BOT_TOKEN = "your_bot_token"
   TELEGRAM_API = 12345678
   TELEGRAM_HASH = "your_telegram_api_hash"
   DATABASE_URL = "your_mongodb_url"
   OWNER_ID = 123456789
   UPSTREAM_REPO = "https://github.com/ImKrishana/HKML-X"
   UPSTREAM_BRANCH = "main"
   ```

4. **Commit Changes**
   ```bash
   git add . -f
   git commit -m "thezake"
   ```

5. **Create Heroku App**
   ```bash
   heroku create APP_NAME
   ```

6. **Add Remote**
   ```bash
   heroku git:remote -a APP_NAME
   ```

7. **Set Container Stack**
   ```bash
   heroku stack:set container
   ```

8. **Deploy**
   ```bash
   git push heroku main -f
   ```

9. **Check Logs**
   ```bash
   heroku logs --tail
   ```

</details>

<details>
<summary><strong>VPS/Locally
</strong></summary>

### Prerequisites

Before starting, ensure you have:

- Docker Engine installed ([Installation Guide](https://docs.docker.com/engine/install/))
- Docker Compose v2 installed ([Installation Guide](https://docs.docker.com/compose/install/))
- A Telegram bot token, API ID, API hash, and owner ID
- A MongoDB URL if you want persistence or database-backed features

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/ImKrishana/HKML-X HKML-X
   cd HKML-X
   ```
2. **Create the Configuration File**
   ```bash
   cp config_sample.py config.py
   ```
   Edit `config.py` and set the required values:
   ```python
   BOT_TOKEN = "your_bot_token"
   TELEGRAM_API = 12345678
   TELEGRAM_HASH = "your_telegram_api_hash"
   OWNER_ID = 123456789
   DATABASE_URL = "your_mongodb_url"  # optional
   ```
   qBittorrent reads its profile configuration from `qBittorrent/config/qBittorrent.conf`.
3. **Start the Bot**
   ```bash
   docker compose up -d --build
   ```
4. **Verify the Services**
   ```bash
   docker compose ps
   ```
   The Compose stack starts the bot and a Cloudflare Quick Tunnel. The temporary public URL appears in the tunnel logs:
   ```bash
   docker compose logs -f tunnel
   ```

### Xtras

**View Bot Logs:**
```bash
docker compose logs -f app
```

**View Tunnel Logs:**
```bash
docker compose logs -f tunnel
```

**Restart the Services:**
```bash
docker compose restart
```

**Update and Rebuild:**
```bash
git pull
docker compose up -d --build
```

**Stop the Stack:**
```bash
docker compose down
```
</details>

## Admin Side

The admin commands below are restricted to the bot owner and sudo users.

<details>
<summary><strong>Authorization Management</strong></summary>

### Authorize Users/Chats

Authorize the current chat:
```
/authorize
```

Authorize a specific chat or user:
```
/authorize CHAT_ID
```

Authorize a topic in a group:
```
/authorize CHAT_ID|TOPIC_ID
```

### Unauthorize Users/Chats

Unauthorize the current chat:
```
/unauthorize
```

Unauthorize a specific chat or topic:
```
/unauthorize CHAT_ID
/unauthorize CHAT_ID|TOPIC_ID
```

### Add Sudo Users

Add a sudo user by ID or reply to their message:
```
/addsudo USER_ID
```

### Remove Sudo Users

Remove a sudo user by ID or by replying to their message:
```
/rmsudo USER_ID
```

### Blacklist Users

Permanently blacklist a user:
```
/blacklist USER_ID
```
Temporarily blacklist a user (time units: `d`, `h`, or `m`):
```
/blacklist USER_ID -t 1d
```
You can also reply to a user's message and use `/blacklist -t 2h`.

### Remove a User from the Blacklist

Remove a user by ID or by replying to their message:
```
/rmblacklist USER_ID
```
</details>

<details>
<summary><strong>Broadcast System</strong></summary>

Reply to a message and broadcast it to users who have started the bot:
```
/broadcast
```

**Forward with the original sender tag:**
```
/broadcast -f
```

**Send quietly:**
```
/broadcast -q
```

**Edit a broadcast** by replying with the edited message and its broadcast ID:
```
/broadcast BROADCAST_ID -e
```

**Delete a broadcast:**
```
/broadcast BROADCAST_ID -d
```

| Flag | Description |
|---|---|
| `-f` or `-forward` | Forward with the original sender tag |
| `-q` or `-quiet` | Send without notification sound |
| `-e` or `-edit` | Edit a broadcast using a reply |
| `-d` or `-delete` | Delete a broadcast |

**Important Notes:**
- Broadcasting requires `DATABASE_URL` so the bot can retrieve its private-message users.
- Broadcast IDs can be edited or deleted only until the bot restarts.
- Forwarded messages cannot be edited.
</details>

<details>
<summary><strong>Disclaimer</strong></summary>

Use HKML-X only with content and services you are authorized to access. You are responsible for following applicable laws, copyright rules, and the terms of the services you use.
</details>

---

[![License](https://img.shields.io/github/license/ImKrishana/HKML-X)](https://github.com/ImKrishana/HKML-X/blob/beta/LICENSE)

If you like this project, don't forget to give it a Star !

**Developer:** [ImKrishana](https://github.com/ImKrishana)  
**Base Repo:** [WZML-X](https://github.com/SilentDemonSD/WZML-X)

HKML-X builds on the open-source [mirror-leech-telegram-bot](https://github.com/anasty17/mirror-leech-telegram-bot) and its contributors. The project is distributed under the [GNU Affero General Public License v3.0](LICENSE).
