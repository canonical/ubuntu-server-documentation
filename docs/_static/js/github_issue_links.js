// Add GitHub feedback button to the page
document.addEventListener('DOMContentLoaded', function() {
    // Get github_url from the meta tag
    const githubUrlMeta = document.querySelector('meta[name="github-url"]');
    
    if (!githubUrlMeta) {
        console.warn('GitHub URL not found - feedback button not added');
        return;
    }
    
    const githubUrl = githubUrlMeta.content;

    const link = document.createElement("a");
    link.classList.add("muted-link");
    link.classList.add("github-issue-link");
    link.text = "Give feedback";
    // use the issue template in the .github/ISSUE_TEMPLATE/feedback.yml file
    link.href = githubUrl + "issues/new?template=feedback.yml";
    link.target = "_blank";

    const div = document.createElement("div");
    div.classList.add("github-issue-link-container");
    div.append(link)

    // Try multiple possible container locations (Furo theme structure)
    const possibleContainers = [
        '.article-container > .content-icon-container',
        '.content-icon-container',
        'article header',
        '.page-content article',
        'main article'
    ];
    
    let container = null;
    for (const selector of possibleContainers) {
        container = document.querySelector(selector);
        if (container) {
            console.log('Found container with selector:', selector);
            break;
        }
    }
    
    if (container) {
        container.prepend(div);
    } else {
        console.warn('Could not find suitable container for feedback button');
        console.log('Available elements:', document.querySelector('article')?.className);
    }
});
