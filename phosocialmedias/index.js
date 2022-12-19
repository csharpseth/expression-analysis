const express = require('express');
const app = express();
const postdata = require('./postdata.json')
const port = 80;

let currentSentiment = 
{
    sentiment: 'neutral',
    face: false
}

app.use(express.static('public'))

const Random = (min, max) => {
    return min + Math.floor(Math.random() * max)
}

const GetRandomPost = () => {
    usernames = postdata[0].usernames
    posts = postdata[1].posts
    locations = postdata[3].locations
    poststats = postdata[4].poststats
    dates = postdata[5].dates
    profiles = postdata[6].profiles

    usernameIndex = Random(0, usernames.length)
    username = usernames[usernameIndex]

    postIndex = Random(0, posts.length)
    post = posts[postIndex]

    postUrl = post.imageurl

    commentIndex = Random(0, poststats.length)
    comments = poststats[commentIndex]
    
    dateIndex = Random(0, dates.length)
    date = dates[dateIndex]

    likeIndex = Random(0, poststats.length)
    likes = poststats[likeIndex]

    descIndex = Random(0, post.description.length)
    description = post.description[descIndex]

    locationIndex = Random(0, locations.length)
    location = locations[locationIndex]

    profileIndex = Random(0, profiles.length)
    profile = profiles[profileIndex]


    postObj = {
        user: username,
        pic: profile,
        desc: description,
        location: location,
        comments: comments,
        likes: likes,
        date: date
    }

    return postObj
}

let polled = []

const GetRandomVideoPost = () => {
    data = GetRandomPost()
    vids = postdata[7].videos
    urlIndex = Random(0, vids.length)

    polls = 0
    while(polled.includes(urlIndex))
    {
        urlIndex = Random(0, vids.length)
        polls++
        if(polls >= vids.length)
            break
    }
    polled.push(urlIndex)

    url = vids[urlIndex]

    post = {
        user: data.user,
        pic: data.pic,
        desc: data.desc,
        location: data.location,
        comments: data.comments,
        likes: data.likes,
        date: data.date,
        url
    }

    return post
}

app.get('/getpost', (req, res) => {
    post = GetRandomPost()
    res.json(post)
});

app.get('/getvideopost', (req, res) => {
    post = GetRandomVideoPost()
    res.json(post)
});

app.get('/sentiment', (req, res) => {
    res.json(currentSentiment)
})

app.post('/sentiment', (req, res) => {
    currentSentiment.sentiment = req.query.s
    if(req.query.f == 'True')
        currentSentiment.face = true
    else
        currentSentiment.face = false
    console.log(req.query);
    res.end()
})

app.listen(port, () => {
    console.log(`Successfully Started Server On Port: ${port}`);
});