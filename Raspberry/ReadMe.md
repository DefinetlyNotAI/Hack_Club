
# 📝 Pwnagotchi AutoPcap Plugin README

## 🎯 Overview
🔗 The AutoPcap plugin for Pwnagotchi automates the process of capturing and uploading `.pcap` files to Discord via a webhook. This plugin is particularly useful for those looking to streamline their workflow and enhance their cybersecurity practices.

## 📦 Installation

### 🖥️ Prerequisites

- Make sure Pwnagotchi is set up and running correctly without plugins.
- If you are using linux, set experimental to true, else leave it false for windows as it will use wsl.

### 🚀 Steps
1. Clone this repository or download the plugin script.
2. Place the `AutoPcap.py` script in the `/usr/local/share/pwnagotchi/custom-plugins/` directory on your SD card.
3. Edit your Pwnagotchi configuration file located at `/etc/pwnagotchi/config.toml` to enable custom plugins by adding or modifying the line:
   ```toml
   main.custom_plugins = "/usr/local/share/pwnagotchi/custom-plugins/"
   ```

## 🛠️ Configuration

### 📄 config.json
Create a `config.json` file in the same directory as your plugin with the following structure:
```json
{
  "webhookUrl": "YOUR_DISCORD_WEBHOOK_URL_HERE"
}
```
Replace `"YOUR_DISCORD_WEBHOOK_URL_HERE"` with your actual Discord webhook URL.

## 🚦 Usage
Once installed and configured, the AutoPcap plugin will automatically start capturing `.pcap` files 
and uploading them to Discord whenever a handshake is detected. 
The plugin logs all activities, making it easy to track its progress and troubleshoot any issues.

The plugin is able to upload `pcap` files only if connected to the internet. 
To do that follow this [guide](https://www.youtube.com/watch?v=z5yb43PlhEA)

## 🐛 Troubleshooting

If you encounter any issues, check the following:
- Ensure your `config.json` file is correctly formatted and contains a valid Discord webhook URL.
- Verify that Pwnagotchi is configured to use custom plugins.
- Check the plugin logs for any error messages.

## 📈 Contributing

Contributions are welcome! Feel free to fork the repository, make your changes, and submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📢 Acknowledgments

- Special thanks to the Pwnagotchi community for their support and inspiration.

## ⚙️ Advanced Configuration
While the basic setup gets you started, 
the AutoPcap plugin offers several advanced configuration options
to tailor its behavior to your specific requirements.

### Logging

The plugin supports detailed logging to help monitor its operation and troubleshoot issues.
By default, logs are saved to `Server.log`. 
You can adjust the log filename and maximum size by modifying the plugin's initialization parameters.

```python
AutoPcap.Log(filename="CustomLogName.log", max_size=5000)
```

### Customizing Webhook Behavior

If you wish to customize the webhook payload sent to Discord,
you can modify the `send_pcap_files_to_discord` function within the plugin.
This allows you to change the message content, embeds, or even add additional files.

## 🛠️ Troubleshooting Tips

Here are some common issues and solutions to help you get back on track:

### Plugin Not Loading
- Ensure the plugin is placed in the correct directory as specified in your Pwnagotchi configuration file.
- Verify that the `config.toml` file has been correctly updated to include the path to custom plugins.

### Discord Upload Fails
- Check your internet connection to ensure it's stable.
- Verify the webhook URL in your `config.json` file is correct and active.
- Ensure the Discord channel associated with the webhook allows file uploads.

### Log File Issues
- If the log file grows too large, consider reducing the `max_size` parameter or implementing a log rotation mechanism.

## ❓ Frequently Asked Questions

### Can I use multiple webhook URLs?
Currently, the plugin supports one webhook URL at a time.
However, you can modify the source code to iterate through a list of webhooks if needed.

### How do I update the plugin?
To update the plugin, replace the existing `AutoPcap.py` script in the `/usr/local/share/pwnagotchi/custom-plugins/` 
directory with the new version. Remember to restart Pwnagotchi to apply the changes.

### Is there a way to filter which `.pcap` files are uploaded?
Yes, you can customize the `on_handshake` function to include logic that filters `.pcap` files based on criteria such as file size, SSID, or timestamp.

## 📢 Support and Community
If you encounter issues not covered here or wish to discuss feature requests, consider joining the Pwnagotchi community forums or Discord channels. The community is active and always willing to help.

## 🌟 Giving Back
If you find the AutoPcap plugin useful, please consider giving back by contributing to the project, 
sharing your experiences, or supporting the developers through donations.

## 📚 Additional Resources
- Pwnagotchi Official Documentation: [https://pwnagotchi.net/](https://pwnagotchi.net/)
- Discord Developer Portal: [https://discord.com/developers/docs](https://discord.com/developers/docs)
