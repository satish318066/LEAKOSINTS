
# LeakOSINT Telegram Bot

## Features
- 🔍 Normal & Advanced Search using LeakOSINT API
- 💰 Coin system (referral, deduct per search)
- 🎁 Redeem code system
- 👑 Admin commands via Telegram
- 📊 Referral & query tracking

## Deployment (Railway Preferred)
1. Go to [https://railway.app](https://railway.app)
2. Create an account
3. Click 'New Project' > 'Deploy from GitHub' or 'Deploy from Template'
4. Set these environment variables:
   - `BOT_TOKEN`
   - `ADMIN_ID`
   - `API_TOKEN`
5. Deploy and your bot will run 24/7!

## Run Locally (Termux/PC)
```bash
pip install -r requirements.txt
cp .env.example .env
# Fill your .env values
python main.py
```
