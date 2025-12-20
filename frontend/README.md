# Frontend Technical Specification

- Create a static website that serves an HTML resume.

## Resume Format Considerations

I live in Canada, where resumes in Word or PDF format should exclude information that could be used to discriminate against potential candidates (e.g. sex, age). Some companies even redact the candidates named to prevent any bias. However, for a personal website or LinkedIN profile, this is acceptable.

In Canada we use a format similar to the most common in the US.

I'm going to use the [Harvard Resume Template format](https://careerservices.fas.harvard.edu/channels/create-a-resume-cv-or-cover-letter/#uc_resource_titles-4) as the basis of my resume.

## Harvard Resume Format Generation

I learned HTML by coding in Notepad back when GeoCities existed, but stopped once WYSIWYG editors became a thing. I'll use GenAI tools to generate the HTML and CSS. Once that is in place, I can adjust the code as needed for the project. Since I have a Pro account, I'll be using Claude Sonnet 4.5 to construct the HTML and add in content from my existing resume.

Prompt to Claude

```text
Convert this resume format into html.
Please don't use a css framework.
Please use the least amount of css tags
```

![Harvard Resume Format Template](./docs/harvard-resume-format.jpg)

This is the [generated output](./docs/nov-23-2025-resume-minimal.html) that I will refactor with Claude.

This is the generated HTML from Claude Sonnet 4.5

![Rendered resume using minimal HTML template](./docs/resume-minimal-rendered.png)

That actually looks good and pretty close to what I want.

To save time I decided to uploaded my current resume to Claude and had it fill in my info using the Harvard template.

Prompt to Claude

```text
I am now uploading the most recent copy of my resume. 
Using the Harvard template you already have, let's create a new resume.
Remember to Convert this resume format into html. 
Please don't use a css framework. 
Please use the least amount of css tags
```

I find that reminding AI, or repeating your prompts, improves your results. Just as if you were talking to a person and giving them clear instruction for a task.

![Resume populated with my information using Claude](./docs/claude-resume-minimal-rendered.png)

## HTML Adjustments

- UTF8 will support most languages. I plan to use only English but will keep the meta tag in.
- To ensure the is the site is viewable on mobile devices, we'll include the viewport meta tag width=device-width
- I will simplify the HTML markup css selector to be as minimal as possible
- I will use the [W3c Validation Service](https://validator.w3.org/) to lint the code.

![W3C validation results showing no errors](./docs/w3c-code-validation.png)

No errors. Score one for GenAI.

The code is also very easy to read and I feel that I could edit by hand without breaking a table or CSS.

## Server Static Website Locally

I need to server my static website locally so I can start using stylesheets externally from my HTML page in a DEV environment. I'm going to use the [Live Server Extension for VScode](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) to work on this locally. You can install an http server in CodeSpaces, but in case there are issues I don't want to waste time troubleshooting when local Just Works.

CSS can be a challenge for me as I don't have an eye for design, but I know what looks good. I'll use Claude Code to do the dirty work and I'll adust as needed. Here's an example of a PR that Claude Code creates for you.

![Claude Code generated pull request example](./docs/claude-code-pr.png)

## FrontEnd Considerations

I attempted to use React and Vite to my Frontend, but found I was spending more time troubleshooting the setup than actually developing. Since I intended to update the site regularly, it makes senses to use something simple and I can update myself with little effort.

## Working with Claude Code

I find my Project Management experience serves me well when it comes to to having GenAI create the basic HTML and CSS. It's great to have a tool that I can give a detailed task to and have it completed with little need for adjustments. It can work on a request and create the PR so I can review it and make adjustments.

As you see here, I'm using new chat sessions for each PR. I'm a big fan of "1 issue, 1 PR" as it makes issue tracking simpler. Claude even puts an issue description in each PR.

![Claude Code assistance workflow showing multiple PRs](./docs/claude-code-assist.png)

That being said, AI goes not "see" well as humans do. Simple describing how I wanted some padding to appear proved challenging. Even if I provided Claude with screenshots, it was just not understanding what I was asking. Giving a detailed description worked but I'm not sure this would work with more complex designs. However the more I worked with it, the better I got at instructing it.

Here I've asked Claude, "Please look at the site in main branch and tell me if we need to clean anything up. Let's make sure we have responsive design, mobile friendly, and easy on the eyes. fonts are clear and easy to read. the page is also accessible for those with visual issues."

![Claude Code accessibility and responsive design review](./docs/claude-code-cleanup.png)