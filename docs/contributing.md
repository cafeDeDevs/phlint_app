# Contribution Guidelines

## Introduction

First and foremost, thank you for contributing to Phlint App! This short
documentation covers conventions and guidelines on how best to make coding
contributioins to Phlint App. While not strictly enforced rules, these
guidelines are meant to provide you with essential standards and practices
common to Open Source Contributions.

## Tickets, Issues, And Bug Fixes

Prior to starting to write code, make sure you're addressing something the
Project Maintainers have determined the project <em>needs</em>. Tickets are
raised based off of needs raised by the Project Lead or Maintainers. Tickets
are also raised by Issues and/or Bugs noticed within the App and then posted
here on Github. Once a Ticket is produced, it's <em>Ticket Number</em> is
assigned to the Issue/Bug here on Github.

Should you volunteer or be assigned to address said Ticket, your Github Handle
will be assigned to the Ticket and Issue, and you will officially be held
responsible for addressing said Ticket/Issue until it is either resolved or you
wish to no longer hold said responsibility and let the Project Lead and other
maintainers know. Once you have taken responsibility for the ticket, please
communicate on the Project Discord roughly how long you project it will take you
to resolve the Ticket, and should you need additional time, please communicate
that as you progress.

## Git Branches

Once you have taken a ticket, ensure that you first pull in the latest updates
from the `main` branch. While within the project directory in your development
environment, pull the updates with the `git pull` command:

```sh
git pull origin main
```

This will ensure that prior to the start of your work, you have all of the
latest updates of the project on your development machine. Next you'll want to
start a new branch and change your development environment to work within that
branch. Naming your new branch should reflect the Ticket/issue. Convention
encouraged for this practice should include the <em>Ticket Number</em>, the
<em>Issue Adddressed</em>, and your <em>Github Handle/Name</em>. An example of
a Ticket with number `001`, Issue Name `add signup to auth`, and handled by
Github user handle name, `tomit4` would look like this:

```sh
001_add_signup_to_auth_tomit4
```

Therefore, creating a new branch and then changing the development environment
to this branch would utilize the `git checkout` command with the `-b` flag like
so:

```sh
git checkout -b 001_add_signup_to_auth_tomit4
```

Once within this git branch, you can know start writing code to address this
ticket/issue.

**Commit Messages:**

As you progress through coding for Phlint, you'll want to keep your code
relegated towards the Issue or Feature you are addressing. Common convention
regarding commit messages is that you should commit <em>often</em>. Even if
your commit is rather mundane like making a small note or is just to save
your progress, committing more often is almost always better than committing
less often. This is because a series of commit messages, even if
redundant, can later be <em>squashed</em> to be more concise, but a single
commit with a series of unrelated code can often leave those reading through the
git history questioning exactly what is happening.

A simple commit message will look like:

```sh
git commit -m "Refactored set_cookie function, httponly to false"
```

Commit messages should always start with a <em>capitalized</em> letter, and
should ideally be kept to less than 50 characters. It is important that your
commit messages inform others who might be reading the git history of the
project what was done specifically in that commit. Should you need to simply
save your work, try your best to cover what you are in the middle of. Even a
simple commit message like this:

```sh
git commit -m "Continuing to refactor set_cookie function, in progress"
```

Lets the reader know what you are working on and that the work is, at that time,
not finished. As mentioned earlier, these commits can always be squashed
into one more generalized commit later on during the development lifecycle.

Here I'll make a brief mention on other issues that innevitably come up during coding.
Should you come across any featues/bugs that are unrelated to the Ticket/Issue, simply make a
note of them using `TODO:` or `NOTE:` comments, and create a specific commit
that addresses that unrelated issue. The following example illustrates this
practice:

```python
# TODO: Address Bug that occurs here where signup fails
```

Lastly, you'll notice that other developers working on Phlint make use of Emojis
in their commit messages. This is an aesthetic choice, as emojis can sometimes
be used to give a visual indicator of what kind of ticket/issue this commit
makes. Use of emojis (or "gitmojis") is <em>not</em> a requirement when
committing to Phlint, but should you wish to use them, you can find a small
guide [here](https://gitmoji.dev/). Emojis are added usually to the beginning of
your commit message and do <em>not</em> count towards the 50 character limit.
Here is an example of one in use:

```sh
git commit -m ":recycle: Refactored set_cookie function, httponly to false"
```

Note that you can have multiple commits made before `pushing` your commit up to
the remote repository here on Github. You do <em>not</em> need to push every
time you make a commit, just push up to the repository when you feel you wish to
save to the remote. Also note that until your branch is pulled into `main`, that
you can safely leave unfinished work in your branch, pushed up to github without
fear of altering the `main` branch. One of the nice things about working with
`git` is that it is relatively easy to revert back changes and to fix version
related issues, so don't be afraid of altering the `main` codebase, the Project
Lead will let you know if a branch still needs work before being pulled into the
`main` branch!

## Creating A Pull Request

Testing Workflow
