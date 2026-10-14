# Job Application Assistant

An AI assistant that helps you apply for jobs properly. It gets to know your career first, tells you honestly whether a role is a good fit, then writes a CV and cover letter tailored to that job, ready to send as PDF and Word files. It also helps you prepare for each interview round.

It works inside **Claude Code** or **Codex**, the AI assistants that can work with files on your computer.

## What you get

* **An honest fit check before you spend time applying.** Share a job ad and the assistant tells you where you match, where you fall short, and whether the role suits what you actually want next. You decide whether to go ahead.
* **A CV tailored to each job.** Written from your real experience, never invented. If something important is missing, it asks you rather than guessing.
* **A cover letter** that connects what the employer is asking for to what you have actually done.
* **Ready-to-send documents.** A Word file you can edit and a matching PDF, named neatly for each application.
* **Interview preparation** for every stage, from the first recruiter call to the final round, references and reviewing an offer.
* **An assistant that learns.** When you correct something or say "never write it like that", it remembers for future applications.
* **Everything kept in one folder on your computer.** One folder per application, so you always know what you sent to whom.

## Before you start

You need an AI assistant that can **save files on your computer**. The normal ChatGPT or Claude chat in your browser or phone can't do this, so the skill won't work there.

Use one of these instead:

* **Claude Code**: open the Claude desktop app and switch to the **Code** tab, or use Claude Code in a terminal. It needs a paid Claude plan.
* **Codex**: OpenAI's assistant that works on your computer, available as an app or in a terminal. It needs a paid ChatGPT plan.

Why? This assistant creates and keeps files for you: your career profile, a folder for each job, and the finished CV and cover letter documents. A plain chat window can't do that.

## How to install

1. Open Claude Code or Codex.
2. Paste this message and send it:

   ```
   Install this skill for me: https://github.com/sartor-n/job-application-skill
   ```

3. The assistant handles the setup. If it asks permission to install something, it's needed to create the PDF and Word documents, so say yes.
4. When it says it's done, start a new conversation so the assistant picks up the new skill.

## How to use it

Just talk to it. For example:

* "Help me apply for this job: *paste the link or the job ad*"
* "Prepare me for my recruiter call for the job at *company*"
* "I have the final interview tomorrow, help me get ready"
* "I got an offer, help me review it"

**The first time** you use it, the assistant runs a one-off setup conversation to get to know your career, your strengths and what you're looking for. It takes roughly 20 to 40 minutes, a bit less if you have an existing CV to share. Talking out loud using your device's voice input is often quicker and gives richer answers than typing. You only do this once. After that, each new job takes a few minutes of your time.

## Good to know

* **It won't make things up.** If it doesn't know enough about part of your background to write about it accurately, it stops and asks. That's on purpose.
* **You stay in control.** It always shows you the fit check and waits for your go-ahead before writing anything.
* **Your information stays on your computer,** in a folder called `job-applications` in your home folder. Nothing is published anywhere.
* **You can edit the documents yourself.** Change the Word file however you like, then ask the assistant to make a fresh PDF from it.
* **Want to see an example first?** The `examples` folder has a finished application for a made-up person, Sam Okafor.

## Licence

Free to use and share under the [MIT licence](LICENSE).

---

### For the AI assistant doing the installation

Follow [INSTALL.md](INSTALL.md). It covers where the skill goes, what to install, how to check that it works, and what to tell the user afterwards. Keep your messages to the user non-technical.
