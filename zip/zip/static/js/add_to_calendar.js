import { atcb_action } from "https://cdn.jsdelivr.net/npm/add-to-calendar-button@2.9.1/+esm";

const button = document.querySelector("#add-to-calendar");

const defaultConfig = {
  organizer: "Za in proti|info@zainproti.si",
  options: [
    "Apple",
    "Google",
    "iCal",
    "Microsoft365",
    "MicrosoftTeams",
    "Outlook.com",
    "Yahoo",
  ],
};

const config = { ...defaultConfig, ...window.__EVENT_CALENDAR_OPTIONS__ };

button.addEventListener("click", () => atcb_action(config, button));
