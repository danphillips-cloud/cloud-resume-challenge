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

![](./docs/harvard-resume-format.jpg)

This is the [generated output](./docs/nov-23-2025-resume-minimal.html) that I will refactor with Claude.

This is the generated HTML from Claude Sonnet 4.5

![](./docs/resume-minimal-rendered.png)

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

![](./docs/claude-resume-minimal-rendered.png)

## HTML Adjustments


- UTF8 will support most languages. I plan to use only English but will keep the meta tag in.
- To ensure the is the site is viewable on mobile devices, we'll include the viewport meta tag width=device-width
- I will simplify the HTML markup css selector to be as minimal as possible
- I will use the [W3c Validation Service](https://validator.w3.org/) to lint the code.

![](./docs/w3c-code-validation.png)

No errors. Score one for GenAI.

The code is also very easy to read and I feel that I could edit by hand without breaking a table or CSS.

## Server Static Website Locally

I need to serve my static website locally so I can work with external stylesheets in a DEV environment. I'm using the [Live Server Extension for VSCode](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) for this. Sure, you can install an http server in CodeSpaces, but I'd rather not waste time troubleshooting when local dev just works.

CSS isn't my strong suit—I don't have an eye for design, though I know what looks good. That's where Claude Code comes in to handle the heavy lifting while I fine-tune. Here's an example PR that Claude Code generates:

![](./docs/claude-code-pr.png)

## FrontEnd Considerations

I initially tried using React and Vite for the frontend, but found myself spending more time troubleshooting setup than actually building. Since I plan to update the site regularly, keeping things simple made more sense—something I can maintain and update without friction.

## Working with Claude Code

My Project Management background pays dividends when working with GenAI to generate HTML and CSS. It's powerful having a tool that can take detailed requirements, execute them, and create a PR ready for review and adjustments.

As you can see, I'm using separate chat sessions for each PR. I'm a big believer in "1 issue, 1 PR"—it keeps issue tracking clean. Claude even auto-generates issue descriptions in each PR.

![](./docs/claude-code-assist.png)


That said, AI doesn't "see" the way humans do. Simple tasks like describing how I wanted padding to appear proved surprisingly difficult. Even with screenshots, Claude struggled to grasp what I wanted. Detailed written descriptions worked better, though I'm skeptical this approach would scale to more complex designs. The upside? The more I worked with it, the better I got at giving clear instructions.

Here I asked Claude: "Please look at the site in main branch and tell me if we need to clean anything up. Let's make sure we have responsive design, mobile friendly, and easy on the eyes. Fonts are clear and easy to read. The page is also accessible for those with visual issues."

![](./docs/claude-code-cleanup.png)

After all these branches and changes, I did my own code review and found things were messy. I went back to Claude to address issues like:
- Eliminating inline styles and improving structure
- Consistent naming and formatting
- Clear comments and documentation
- CSS variables and DRY principles
  
There's still some navigation/SVG duplication and other optimizations to tackle, but I'll leverage AWS/GCP tooling for that.