# Environment Setup for CTAS

## Required API Credentials

To run CTAS properly, you'll need to set up the following API credentials:

### Twilio (SMS Alerts)
1. Create an account at [Twilio](https://www.twilio.com)
2. Get your Account SID and Auth Token from the Twilio dashboard
3. Purchase a phone number for sending SMS alerts

### Environment Configuration

1. Create a `.env` file in the backend directory using `.env.example` as a template
2. Add your API credentials to the `.env` file:

```
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
API_KEY=your_api_key
```

⚠️ **IMPORTANT SECURITY WARNING** ⚠️
- Never commit your `.env` file to version control
- Never share API keys or tokens in code, chat, or public forums
- Regularly rotate your API credentials as a security best practice
- Use environment variables instead of hardcoding credentials
