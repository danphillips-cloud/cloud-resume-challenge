# Frontend Techincal Specification

- Create a static website that serves an HTML resume. 

## Resume Format Considerations

I live in Canada, where resumes in Word or PDF format should exclude information that could be used to discriminate against potential candidates. However, a personal website or LiknedIN profile, this is acceptable. 

In Canada we use a format similar to the most common in the US. 

I'm going to use the [Harvard Resume Template format](https://careerservices.fas.harvard.edu/channels/create-a-resume-cv-or-cover-letter/#uc_resource_titles-4) as the basis of my resume. 

## Harvard Resume Format Generation

I know HTML well, but stopped coding it when WYSIWYG editors became a thing. I'm going to use GenAI tools to generate the HTML and CSS. Once that is in place, I can adjust the code as needed for the project. I'm using Claude Sonet 4.5 for the html. 

Prompt to Claude

```text
Convert this resume format into html.
Please don't use a css framework.
Please use the least amount of css tags
````

![](./docs/harvard-resume-format.jpg)

This is the [generatated output](./docs/nov-23-2025-resume-minimal.html) that I will refactor with Claude. 

This is what the generated HTML from Claude Sonet 4.5

![](./docs/resume-minimal-rendered.png)

To save time I decided to uploaded my current resume to Claude and had it fill in my info using the Harvard template. 

![](./docs/claude-resume-minimal-rendered.png)

## HTML Adjustments

- UTF8 will suport most lanauages. I plan to use only English but will keep the meta tag in. 
- To ensure the is the site is viewable on mobile devides, we'll include the viewport meta tag width=device-width
- I will extract our styles into it's own style sheet after I am happy with the HTML markup. 
- I will simplify the HTML markup css selector to be as minnmal as possible. 


