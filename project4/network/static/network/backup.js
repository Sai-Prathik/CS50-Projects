document.addEventListener("DOMContentLoaded",()=>{
    document.querySelector("#all").addEventListener("click",()=>load_posts());
   document.querySelector("#following").addEventListener("click",()=>load_following());
   document.querySelector("#profile").addEventListener("click",()=>load_profile("user"));
   load_posts("user");
   document.querySelector("#search_bar").onsubmit=()=>search_profile();
  });

function load_posts(){
document.querySelector("#posts").style.display="block";
document.querySelector("#following_page").style.display="none";
document.querySelector("#profile_page").style.display="none";
document.querySelector(".search_results").style.display="none";
document.querySelector("#title").innerHTML="All Posts";
document.querySelector("#text").onkeyup=()=>{
    if(document.querySelector("#text").value.length>0){
        document.querySelector(".post").disabled=false;
    }
    else{
      document.querySelector(".post").disabled=true;
    }
}
document.querySelector(".post").disabled=true;
document.querySelector("#create_post").onsubmit=()=>{
    var val=document.querySelector("#text").value;
     fetch("posts/",{
        method:'POST',
        body:JSON.stringify({
            posts:val
        })
    }).then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }); 

    fetch("get_posts/posts")
.then(response=>response.json())
.then(posts=>{
     display_posts(posts,"index-page");
});

}
}

function load_following(){
  document.querySelector("#posts").style.display="none";
document.querySelector("#following_page").style.display="block";
document.querySelector("#profile_page").style.display="none";
document.querySelector("#title").innerHTML="Following";
}

function load_profile(status){
  document.querySelector("#posts").style.display="none";
document.querySelector("#following_page").style.display="none";
document.querySelector("#profile_page").style.display="block";
document.querySelector(".search_results").style.display="none";
document.querySelector("#title").innerHTML="Profile";
fetch("get_posts/profile")
.then(response=>response.json())
.then(posts=>{
  if(status=="user"){
      document.querySelector(".follow").innerHTML="Edit Profile";
      
      display_posts(posts,"profile");
  }
  else if(status=="follower"){
      document.querySelector(".follow").innerHTML="Follow";
       
  }
     
});

}

function removeAllChildNodes(parent){
  while(parent.firstChild){
      parent.removeChild(parent.firstChild);
  }
}


function display_posts(posts,type){
 
  if(posts.length<1){
      document.querySelector(".post-list").style.display="none";
  }
  else{
  var post_list="";
  if(type==="profile"){
      post_list=document.querySelector(".post-list");
       
  }
  else if(type==="index-page"){
      post_list=document.querySelector(".index-page");
      
  }
  
  
  removeAllChildNodes(post_list);
  posts.forEach(element => {
      var image=new Image();
      image.src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png ";
      image.style.width="10%";
      image.style.height="5%";
      image.style.marginRight="10px";

      var div=document.createElement("div");
      div.append(image);

      var user=document.createElement("div");
      user.innerHTML=`${element.author}`
      user.className="title";
      user.style.fontSize="140%";
      user.style.fontWeight="bolder";
      user.style.display="inline";
      div.append(user);

      var time=document.createElement("div");
      time.innerHTML=`${element.time_stamp}`
      div.append(time);
      time.style.display="inline-block";
      time.style.float="right";

      var post=document.createElement("div");
      post.innerHTML=`${element.post}`;
      div.append(post);
      post.style.marginTop="10px";
      post.style.marginLeft="12%";
      post.style.fontSize="150%";

      var like=new Image();
      like.src="http://assets.stickpng.com/thumbs/585e4e6ccb11b227491c339e.png";
      div.append(like);
      like.style.width="7%";
      like.style.cursor="pointer";

      var likes=document.createElement("div");
      likes.innerHTML=`${element.likes}`;
      likes.style.fontSize="120%";
      likes.style.display="inline-block";
      div.append(likes);
      
      //like.style.display="inline-block";
      div.className="card_design"
      div.style.borderStyle="solid";
      div.style.padding="10px";
      div.style.width="100%";
      
      div.style.borderColor="#00acee"
      div.style.color="white";
      div.style.display="block";
      div.style.borderRadius="15px";

      post_list.style.top="110%";
      post_list.style.left="0%";
     
      post_list.append(div);
      
  });
}
}

function search_profile(){
  var val=document.querySelector("#search_key").value;
  fetch("get_posts/search_profile",{
      method:'POST',
      body:JSON.stringify({
          search_key:val
      })
  }).then(response=>response.json())
  .then(posts=>{
          load_search_results(posts);
  });
   
}

function load_search_results(posts){

document.querySelector("#posts").style.display="none";
document.querySelector("#following_page").style.display="none";
document.querySelector("#profile_page").style.display="none";
document.querySelector(".search_results").style.display="block";
document.querySelector("#title").innerHTML="Search Results";
var results=document.querySelector(".search_results");
results.style.position="relative";
results.style.left="32%";
results.style.top="40px";

results.style.display="block";
results.style.width="30%";
removeAllChildNodes(results);
posts.forEach(element=>{
      var profile_card=document.createElement("div")

      var img=new Image();
      img.src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7e/Circle-icons-profile.svg/1200px-Circle-icons-profile.svg.png";
      img.style.width="10%";
      img.style.height="5%";
      img.style.marginRight="10px";
      profile_card.append(img);
      var username=document.createElement("div");
      username.innerHTML=`${element.username}`;
      profile_card.append(username);
      username.style.display="inline";
      username.style.position="relative";
      username.style.left="5px";
      profile_card.style.borderColor="#00acee";
      profile_card.style.padding="20px";
      profile_card.style.borderStyle="solid";
      profile_card.style.color="white";
      profile_card.style.fontSize="larger";
      profile_card.style.fontWeight="bolder";
      profile_card.style.borderRadius="10px";
      profile_card.style.cursor="pointer";
      profile_card.addEventListener("click",()=>{
          document.querySelector(".user_title").innerHTML=`@${element.username}`;
           
          var s="/get_profile/".concat(element.id);
          fetch(s).then(response=>response.json())
          .then(posts=>{
              load_profile("follower");
                display_posts(posts,"profile");
          });
       
           
      });
      
      results.append(profile_card);
});
}