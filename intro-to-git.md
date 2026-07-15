# Welcome to Git

This is a Git repository hosted on Github. 
Git is a distributed document version management system. 
Distributed means that everyone that "clones" a git repository has their own full working copy. 
A document version management system, means that you can go back in time to any previous snapshot. 
It was designed originally for code, but works very well with other types of documents, especially plain text formats (like markdown, xml, json, csv, etc.)

## Don't Panic

The web interface is ugly and counter intuitive - it was designed for programmers, but could be easily adapted into something nicer and more appropriate for your workflow
Git has a lot of jargon, which could be explained better, especially in other domains.
AI agents make this all almost superfluous (

## The Vernacular of Git

Git is easiest learned throught the command line interface (CLI). 

The most important git commands are:

`git clone <url>` - create a folder on my computer that contains a copy of a remote repository that can be easily synced
`git add .` - Add all changed to the "staging area"  
`git commit -m "My message"` - Creat a snapshot of all files in the "staging area" with a message and a unique ID called the commit hash 
`git push` - Push my latest commits to the remote server (if out of date, Git will tell you, and will pull)
`git pull` - Get the latest changes from the remote server and merge automatically if you can 

The "staging area" is just a list of all files currently being tracked as the current change set (to be commited in the next commit) 

## Github

Github is a server for hosting Git repositories with a set of web-based tools for doing advanced workflows and edting. 
Typically you don't put binaries in a Git repository, but there are some use cases for that. 
There is a hard limit of 100MB in Github unless you enable Git LFS (Large File Storage). 
A common workflow is to have a single source of truth hosted on a server (e.g., on Github).
Every collaborator clones the repo locally on their computer. 
The server version is called the "remote" or "upstream". 

When theya user makes changes on their own version they are creating a new timeline.
When they want they can push their version to remote server. 
If the remote is out of sync  (meaning some synchronization) to be done they will be required to first: 
1. Pull remote changes
2. Merge the current changes (which happens automatically unless a conflict happens). 

## Branches 

So far we are assuming everyone is working on the same "branch" (usually called main). 
Git has the advantage that it is very easy to create and switch between lightweight "branches" which are effectively different version histories maintained in the same repo.
They are like alternate timelines, which you can "merge" together.
You can use them to develop features in isolation, that you can push to the remote server, without synchronization.
Multiple people can collaborate on any branch in the same way they can on main.
This could be useful if teams need to work on a certain aspect of a design, without interuption.

## Merge Conflicts

This is an advanced topic, and it only happens when two people change the same document on the same line and Git can't 
automatically figure out how to combine the two changes. You have to resolve changes. At this point I would suggest asking for 
help, or watching some videos on how to resolve merge conflicts. My favorite tool for this purpose is VS Code.
