document.addEventListener("DOMContentLoaded",()=>{
    
    document.querySelector("body").style.backgroundColor="#192841";
    document.querySelector("#profile").addEventListener("click",()=>profile("user"));
    document.querySelector("#all").addEventListener("click",()=>all_posts());
    document.querySelector("#following").addEventListener("click",()=>following());
    document.querySelector("#search_bar").addEventListener("submit",(e)=>{
        e.preventDefault();
        search_results();
    });
    
    all_posts();
});
    

 
function all_posts(){
     document.querySelector("#title").innerHTML="All Posts";
     document.querySelector("#profile-page").style.display="none";
     document.querySelector("#following-page").style.display="none";
     document.querySelector("#posts").style.display="block";
     document.querySelector("#search-results").style.display="none";
     document.querySelector("#edit-page").style.display="none";
     var b=document.querySelector("#post-input")
     document.querySelector("#post-input").onclick=()=>{b.style.border="solid #1DA1F2"}


      
     document.querySelector("#post-form").addEventListener("submit",()=>{
          console.log("posted");
          fetch("posts/",{
             method:"POST",
             body:JSON.stringify({
                 posts:document.querySelector("#post-input").value
             })
         });
     });

    fetch("get_posts/posts").then(response=>response.json()).then(posts=>{
        console.log(posts);
         load_posts(posts,"all_posts");
    });
    document.querySelector("#all_posts").innerHTML="";

}

function profile(status,name=null){
    document.querySelector("#title").innerHTML="Profile";
    document.querySelector("#posts").style.display="none";
    document.querySelector("#following-page").style.display="none";
    document.querySelector("#profile-page").style.display="block";
    document.querySelector("#search-results").style.display="none";
    document.querySelector("#edit-page").style.display="none";
    if(status=="user"){fetch("get_posts/profile").then(response=>response.json()).then(
        elements=>{
                 elements.forEach(element=>{
                       window.p=element.username;
                     document.querySelector("#username").innerHTML=`@${element.username}`;
                     document.querySelector("#follow").style.display="none";
                     document.querySelector("#edit-profile").style.display="block";
                     document.querySelector(".followers").innerHTML=`<span>${element.followers} followers</span> <span>${element.following} following</span> `
                     fetch(`get_profile/${element.id}`).then(response=> response.json()).then(post=>{
                        console.log(post);
                         load_posts(post,"profile");
                           
                    })});
                    });

     
}
else{                
                     document.querySelector("#title").innerHTML=`${name.username}`;
                     document.querySelector("#username").innerHTML=`@${name.username}`;
                     if(name.username==window.p){
                         
                        document.querySelector("#follow").style.display="none";
                        document.querySelector("#edit-profile").style.display="block";
                     }else{
                         
                        document.querySelector("#follow").style.display="block";
                        document.querySelector("#edit-profile").style.display="none";
                        

                     }
                     if(name.relation==true){
                        document.querySelector("#follow").innerHTML="Unfollow";
                        
                        
                     }
                     else if(name.relation==false){
                        document.querySelector("#follow").innerHTML="Follow";
                         
                        
                     }
                     document.querySelector(".followers").innerHTML=`<span>${ name.followers} followers</span> <span>${name.following} following</span> `;
                     fetch(`get_profile/${name.id}`).then(response=> response.json()).then(post=>{
                        console.log(post);
                         load_posts(post,"profile"); 
                    });
                     document.querySelector("#follow").onclick=()=>{
                        
                         if(document.querySelector("#follow").innerHTML=="Follow"){
                             console.log("followed")
                            document.querySelector("#follow").innerHTML="Unfollow";
                            /*window.f_y-=1;*/
                            fetch(`follow/${name.id}/follow`);
                            name.followers+=1;
                            document.querySelector(".followers").innerHTML=`<span>${ name.following} followers</span> <span>${name.followers} following</span> `;
                         }
                         else if(document.querySelector("#follow").innerHTML=="Unfollow"){
                            console.log("Unfollowed")
                            document.querySelector("#follow").innerHTML="Follow";
                            fetch(`follow/${name.id}/Unfollow`);
                            name.followers-=1;
                            document.querySelector(".followers").innerHTML=`<span>${ name.followers} followers</span> <span>${name.following} following</span> `;
                            
                         }
                         
                     }
                     fetch(`get_profile/${name.id}`).then(response=> response.json()).then(post=>{
                        console.log(post);
                         
                     load_posts(post,"profile");
                    });
                     
                    document.querySelector(".posts").innerHTML="";
}

    
    
                 
}
function following(){
    document.querySelector("#title").innerHTML="Following";
    document.querySelector("#profile-page").style.display="none";
    document.querySelector("#posts").style.display="none";
    document.querySelector("#following-page").style.display="block";
    document.querySelector("#search-results").style.display="none";
    document.querySelector("#edit-page").style.display="none";
}

function load_posts(posts,page_name){
    //console.log(status);
    posts.forEach(elements=>{
         console.log(page_name);
        const b=document.createElement("div");
        img=new Image()
        img.src='https://image.flaticon.com/icons/png/128/3011/3011270.png';
        img.style.width="7%";
       
        var title=document.createElement("div");
        title.innerHTML=elements.author;
        title.style.display="inline";
        title.style.color="white";
        title.style.fontWeight="bolder";
        title.style.fontSize="large";
        title.style.position="relative";
        title.style.left="10px";

        var post=document.createElement("div");
        post.innerHTML=elements.post; 
        post.style.color="white";
        post.style.fontSize="170%";
        post.style.position="relative";
        post.style.left="60px";
        if(page_name=="profile"){
        var edit_button=document.createElement("button");
        edit_button.innerHTML="Edit";
        edit_button.style.display="inline";
        edit_button.style.position="relative";
        edit_button.style.float="right";
        edit_button.style.color="white";
        edit_button.style.borderRadius="10px";
        edit_button.style.padding="5px";
        edit_button.style.border="solid #5de9eb";
        edit_button.style.background="#192841";
        edit_button.style.outline="none";

        edit_button.addEventListener("click",()=>{
            
            edit_page(elements);
        });}


        var likes=document.createElement("div");
        var img1=new Image()
        var status=elements.relation;
        
        if(status==true){
           img1.src="https://image.flaticon.com/icons/png/128/2589/2589175.png";
        }
        else{
            img1.src="https://image.flaticon.com/icons/png/128/833/833300.png";
        }
        img1.onclick=()=>{
             if(status==true){
                fetch(`like_posts/${elements.id}/dislike`);
                status=false;
                elements.likes-=1;
                num_likes.innerHTML=elements.likes;
                img1.src="https://image.flaticon.com/icons/png/128/833/833300.png";
            }
            else if(status==false){
                fetch(`like_posts/${elements.id}/like`);
                status=true;
                elements.likes+=1;
                num_likes.innerHTML=elements.likes;
                img1.src="https://image.flaticon.com/icons/png/128/2589/2589175.png";
            }
        }

        img1.style.width="4%";
        img1.style.border="white";
        img1.style.cursor="pointer";
        
        likes.append(img1);
        likes.style.position="relative";
        likes.style.top="10px";

        var num_likes = document.createElement("div");
        num_likes.innerHTML=elements.likes;
        num_likes.style.position="relative";
        num_likes.style.top="-13px";
        num_likes.style.left="32px";
        num_likes.style.color="white";

        time=document.createElement("div");
        time.innerHTML=elements.time_stamp
        time.style.color="white";
        time.style.display="inline";
        time.style.position="relative";
        time.style.left="30px";
        
        b.append(img);
        b.append(title);
        b.append(time);
        b.append(edit_button);
        b.append(post);
        b.append(likes);
        b.append(num_likes);

        b.style.border="solid #5de9eb";
        b.style.padding="50px";
        b.onmouseenter=()=>{
            b.style.backgroundColor="#1c2e4a";
        }
        b.onmouseleave=()=>{
            b.style.backgroundColor="#192841";
        }
         
        if(page_name=="profile"){
            document.querySelector("#profile_posts").append(b);
        }
        else if(page_name=="all_posts"){
            document.querySelector("#all_posts").append(b);
        }
        
        
    });
    

}

 
 
function search_results(){
    document.querySelector("#title").innerHTML="Search Results";
    document.querySelector("#profile-page").style.display="none";
    document.querySelector("#posts").style.display="none";
    document.querySelector("#following-page").style.display="none";
    document.querySelector("#search-results").style.display="block";
    document.querySelector("#edit-page").style.display="none";
    console.log(document.querySelector("#search-key").value);
    var main=document.querySelector("#results");
    main.style.position="relative";
    main.style.left="27%";
    main.style.top="70px";
    
    fetch("get_posts/search_profile",{
        method:"POST",
        body:JSON.stringify({
            search_key:document.querySelector("#search-key").value
        })
    }).then(response=> response.json()).then(accounts=>{
        accounts.forEach(acc=>{
            console.log(acc);
            var X=document.createElement("div");
            X.style.border="solid #5de9eb"
            X.style.width="40%";
            X.style.padding="30px";
            X.style.cursor="pointer";
            X.onmouseenter=()=>{
                X.style.backgroundColor="#1c2e4a";
             }
             X.onmouseleave=()=>{
                 X.style.backgroundColor='#192841';
             }


             var pp=new Image();
             pp.src="https://image.flaticon.com/icons/png/128/3011/3011270.png";
             pp.style.width="7%";
             

             var user=document.createElement("div");
             user.innerHTML=acc.username;
             user.style.color="white";
             user.style.display="inline";
             user.style.position="relative";
             user.style.left="20px";


             X.append(pp)
             X.append(user);
             main.append(X);
             X.addEventListener("click",()=>{
                profile("visitor",acc);
            });

        });
       
    });
    
    main.innerHTML="";

}

function edit_page(post){
    console.log(post);
    document.querySelector("#title").innerHTML="Edit Post";
    document.querySelector("#profile-page").style.display="none";
    document.querySelector("#posts").style.display="none";
    document.querySelector("#following-page").style.display="none";
    document.querySelector("#search-results").style.display="none";
    document.querySelector("#edit-page").style.display="block";

    document.querySelector("#edit-post-input").innerHTML=post.post;
    document.querySelector("#edit-post-form").addEventListener("submit",(e)=>{
        e.preventDefault();
        fetch("edit_post/",{
            method:"POST",
            body:JSON.stringify({
                id:post.id,
                updated_post:document.querySelector("#edit-post-input").value
            })
        }).then(response=>response.json()).then(console.log("edited"))
    });


}

 
 

