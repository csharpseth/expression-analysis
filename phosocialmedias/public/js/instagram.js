const likePostThreshold = 16

let timer = 10.0
let maxTimer = 10.0

let doTimer = false
let sentiment = 'neutral'
let facePresent = false
let numPositive = 0
let numNegative = 0

let videoEnded = false;

const GetNewPost = () => {
    setTimeout(() => {
        document.querySelector(".post").classList.add("nextpost")
        setTimeout(() => {
            document.querySelector(".post").classList.remove("nextpost")
        }, 900)

        GetPostData()
    }, 800)

}

const GetPostData = () => {
    fetch('/getvideopost')           //api for the get request
        .then(res => res.json())
        .then((data) => setTimeout(UpdatePostView, 200, data))
}

const UpdateProgressVisuals = () => {
    document.getElementById("progress").innerText = `${timer.toFixed(1)}(s) Remaining..`
    width = Math.round((timer/maxTimer) * 100)
    document.getElementById("progressbar").style.width = `${width}%`
}

const ResetClock = () => {
    timer = maxTimer
    UpdateProgressVisuals()
}

const LikePost = () => {
    GetNewPost()
    ResetClock()
    document.getElementById("cover-post-like").classList.add("popinlike")
    setTimeout(() => {
        document.getElementById("cover-post-like").classList.remove("popinlike")
    }, 800)
    numPositive = 0
    doTimer = false
}

const DislikePost = () => {
    GetNewPost()
    ResetClock()
    document.getElementById("cover-post-dislike").classList.add("popinlike")
    setTimeout(() => {
        document.getElementById("cover-post-dislike").classList.remove("popinlike")
    }, 800)
    numNegative = 0
    doTimer = false
}

const GetPostElements = () => {
    let username = document.getElementById("username")
    let extrausername = document.getElementById("extrausername")
    let profilepic = document.getElementById("profile-pic")
    let location = document.getElementById("location")
    //let content = document.getElementById("content-image")
    let content = document.getElementById("video-content")
    let desc = document.getElementById("description")
    let likes = document.getElementById("likes")
    let comments = document.getElementById("view-comments")
    let date = document.getElementById("time-posted")

    let bundle = {
        username,
        extrausername,
        profilepic,
        location,
        content,
        desc,
        likes,
        comments,
        date
    }

    return bundle
}

const InitializePostView = (data, post) => {
    post.content.addEventListener("loadedmetadata", () => {
        maxTimer = post.content.duration - 0.5;
        ResetClock()
        if(facePresent)
        {
            doTimer = true
            post.content.play()
            videoEnded = false
            post.content.addEventListener('ended', () => {
                videoEnded = true
                post.content.src = ''
            })
        }
    })

    document.getElementById("like").onclick = LikePost
    document.getElementById("dislike").onclick = DislikePost
}

const UpdatePostView = (data) => {
    //Get All Elements
    post = GetPostElements()

    //Apply Post data to HTML Elements
    //HEADER
    post.username.innerText = data.user
    post.profilepic.src = `img/profiles/${data.pic}`
    post.location.innerText = data.location
    //content.src = `img/postpics/${data.url}`

    //CONTENT
    post.content.src = `vid/${data.url}`
    console.log(data.url);
    
    //FOOTER
    post.extrausername.innerText = data.user
    post.desc.innerText = data.desc
    post.likes.innerText = `${data.likes} Likes`
    post.comments.innerText = `View all ${data.comments} comments`
    post.date.innerText = data.date

    //This will play the video/start the timer if conditions are met
    InitializePostView(data, post)
}

const DecrementTime = () => {
    if(facePresent == true && doTimer == true)
    {
        timer -= 0.1
        if(timer <= 0.0)
        {
            if(numPositive > likePostThreshold)
                LikePost()
            else
                DislikePost()
            ResetClock()
            return
        }

        UpdateProgressVisuals()
    }
}

const TogglePostCover = (enabled) => {
    visible = "none"
    if(enabled == true) visible = "block"
    document.getElementById("cover-post").style.display = visible
}

const ToggleVideoPlayback = (play) => {
    if(play) {
        post.content.play()
    }else{
        post.content.pause()
    }
}

const UpdateEmote = (state) => {
    let emote = document.getElementById("emote")

    if(state == 'positive')
    {
        emote.src = "img/emote_happy-01.png"
        numPositive++
        if(numPositive > likePostThreshold)
        {
            LikePost()
        }
    }else if(state == 'negative')
    {
        emote.src = "img/emote_mad-01.png"
        numNegative++
        if(numNegative > likePostThreshold)
        {
            DislikePost()
        }
    }else {
        emote.src = "img/emote-01.png"
    }
}

const UpdateSentiment = () => {
    fetch('/sentiment')
        .then(res => res.json())
        .then((data) => {
            sentiment = data.sentiment
            facePresent = data.face
            
            TogglePostCover(!facePresent)
            playVideo = facePresent && (timer > 0.0) && (videoEnded == false)

            ToggleVideoPlayback(playVideo)
            UpdateEmote(sentiment)
        })
}

const Initialize = () => {
    GetPostData()
    setInterval(DecrementTime, 100)
    setInterval(UpdateSentiment, 200)
    setTimeout(() => {
        document.getElementById("progress").innerText = `${timer.toFixed(1)}(s) Remaining..`
        document.getElementById("progressbar").style.width = `100%`
    }, 200)
}

Initialize()