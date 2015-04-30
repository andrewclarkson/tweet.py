[![Build Status](https://travis-ci.org/bitborn/tweet.py.svg?branch=master)](https://travis-ci.org/bitborn/tweet.py)

#Roll your own PaaS

This is a demo combining docker, dokku-alt, and travis CI to create a foolproof push to deploy system.

##Installation

Currently dokku is only really supported on Ubuntu 14.04. Gotta live life on the edge!

###On the server:

There's a bootstrap script in the dokku-alt repo but it defaults to a web based configuration. Generally this just won't work(TM) on an AWS server, so let's do it manually.

Log into root:

    sudo su

Add the docker and dokku-alt sources:

    echo deb https://get.docker.io/ubuntu docker main > /etc/apt/sources.list.d/docker.list
    echo deb https://dokku-alt.github.io/dokku-alt / > /etc/apt/sources.list.d/dokku-alt.list

Add the relevant keys and update:

    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
    apt-key adv --keyserver keys.gnupg.net --recv-keys EAD883AF
    apt-get update -y

Install dokku and docker:

    apt-get install -y dokku-alt

If it asks you to modify local files, keep the local ones.

Check whether docker works

    dokku access:list

If this gives you an "unable to resolve hostname" congrats, AWS broke your instance!

You'll need to add a host to `/etc/hosts` as specified [here](https://forums.aws.amazon.com/message.jspa?messageID=545056)

Then reboot

    sudo reboot

And try again

    dokku access:list

##Configuration

###On your local machine:

Generate a new key pair

    ssh-keygen

This will prompt for a two things, namely:
- The output path (use `/home/<username>/.ssh/<project>`)
- A passphrase (leave it empty)

Now copy the key to the server

    cat ~/.ssh/<project>.pub | ssh [-i <pem file>] <server> sudo dokku access:add

Now we can test pushing a project

Since we're not using the default key pair. We'll have to do a bit of local configuration.

Add the following to `~/.ssh/config`

    Host <server address>
        IdentityFile ~/.ssh/<project>

Note that we're using the private key not `<project>.pub`

Add a remote to the project

    git remote add <name> dokku@<server address>:tweet

Then push

    git push <name> master


###On the server

Note: You'll _need_ a domain to play around with. Deploying to a port doesn't work in dokku

    echo <hostname> | sudo tee /home/dokku/VHOST


## Testing and Travis

###On your local machine

Install the travis gem
    
    gem install travis

Create a travis directory

    mkdir .travis


Create a pem file

    openssl rsa -in ~/.ssh/<project> -outform pem > .travis/<project>.pem

Hide it from git

    echo .travis/<project>.pem >> .gitignore

Create a `.travis.yml` file according to [this guide](http://docs.travis-ci.com/user/build-configuration/#.travis.yml-file%3A-what-it-is-and-how-it-is-used)

Log into travis

    travis login

Encrypt the key 

    travis encrypt-file .travis/<project>.pem --add

For some reason travis adds the encrypted key to the root directory lets move that

    mv <project>.pem.enc .travis

Edit the `.travis.yml` file to reflect the move.
Change `-in <project>.pem.enc` to `-in .travis/<project>.pem.enc`


Add a `after_success:` section like so

    - chmod 600 .travis/<project>.pem
    - mkdir -p ~/.ssh
    - cp .travis/<project>.pem ~/.ssh
    - cat .travis/host >> ~/.ssh/config
    - git remote add production dokku@<server address>:<project>
    - test $TRAVIS_PULL_REQUEST == "false" && test $TRAVIS_BRANCH == "master" && git push <name> master


Then create a `.travis/host` to make travis use the correct key:

    Host <server address>
        StrictHostKeyChecking no
        IdentityFile ~/.ssh/<project>.pem

Then register your project on [travis-ci.org](https://travis-ci.org) and push away.

## Adding Complexity

Add on a database

### On the server

Create the database

    dokku postgresql:create <db>

And link it

    dokku postgresql:link <project> <db>

Then you can get the full url

    dokku config <project>


