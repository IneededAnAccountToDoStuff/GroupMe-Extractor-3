# GroupMe-Extractor-3
It's an extractor for GroupMe using the API. It properly grabs topics and attachments.

I got annoyed at the fact that GroupMe's export data does not grab the messages from subtopics. So I wrote my own. It's been a ~~long~~annoying journey. I started with the API, but could not get it to work. So I tried making an extractor bookmarklet. Eventaully, jumped back to the API. This has been years in the making*. (By that, I mean I've been trying for years. This code was started a few days ago.)

## Getting your API token.
Visit https://dev.groupme.com/

The python script asks you for your token every time. If you use this regularly, I'd recommend editing the .py file with your token.

## How does this work?
This script is based off the [GroupMe API](https://dev.groupme.com/docs/v3). It requests the list of all your chats, then extracts the messages for each chat, extracting topic messages along the way. It then searches the attachments, and extracts them. All of this is packed up into a nice little zip file.

## Is this safe?
For the data passing through, yes. It uses the official GroupMe API, and the data stays local. At no point does any data pass through anything but your computer and GroupMe unencrypted. Unless you don't trust GroupMe, or your browser, or your computer... anyhow, it's as safe as using your browser.

This program doesn't do authentication though. So it may be possible for someone to spoof? I don't really know, not my field of expertise. I may try to fix this later.
