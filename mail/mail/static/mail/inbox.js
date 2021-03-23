document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  
   

  // By default, load the inbox
  load_mailbox('inbox');
});
  
function compose_email( ) {
    
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#mail-view').style.display = 'none';
  // Clear out composition fields
   
    document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  //}
  
  document.querySelector('#compose-body').value = '';

  document.querySelector("#compose-form").onsubmit=()=>{
    var receiver =document.querySelector("#compose-recipients").value;
    
    var subject=document.querySelector("#compose-subject").value;

    var body=document.querySelector("#compose-body").value;

    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: receiver,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    }); 
    alert("Email Sent");

    }
  }
 

 

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-view').style.display = 'none';
    var s="/emails/".concat(mailbox);
      
    fetch(s)
    .then(response => response.json())
    .then(emails => {
        // Print emails
          display_mailbox(emails,mailbox);

        // ... do something else with emails ...
    });
       
        

         
        // ... do something else with emails ...
     
    var a =mailbox.toUpperCase();
    
   document.querySelector("#emails-view").innerHTML=` <h3 id="mail_box">${a}</h3> `;
   var b=document.querySelector("#emails-view").style.color="#1b03a3";
   
   
}



function display_mailbox(emails,mailbox){
  var parent=document.querySelector("#emails-view");
  var child=document.createElement("div");
  child.className="emails";
  parent.append(child);
  emails.forEach(element=>{

      var master=document.createElement("div");
      master.id=`mail${element.id}`;
      master.addEventListener('click',()=>read_mail(element.id));
      var m_id=document.createElement("div");
      m_id.style.fontWeight="bold";
      m_id.style.display="inline-block";
      if(mailbox==="sent"){
        m_id.innerHTML=`${element.recipients}`;
      }
      else{
        m_id.innerHTML=`${element.sender}`;
      }

       
      
      var sub=document.createElement("div");
      sub.innerHTML=`${element.subject}`;
      sub.style.marginLeft="auto";
      //sub.style.marginLeft="250px";
      master.append(element.sender);
      master.append(sub);

      var time=document.createElement("div");
      time.innerHTML=`${element.timestamp}`;
      time.style.marginLeft="auto";
      master.append(time);
      var arch=document.createElement("button");
      if(element.archived){
        arch.innerHTML="Unarchive";
      }
      else{
        arch.innerHTML="Archive";
      }
      arch.style.margin="auto";
      arch.className="btn btn-sm btn-outline-primary"
      arch.addEventListener("click",()=>{
        var s="/emails/".concat(element.id);
        if(element.archived){
          
          fetch(s, {
            method: 'PUT',
            body: JSON.stringify({
                archived: false
            })
          });
          alert("Message unarchived");
        }
        else{
          arch.innerHTML="Archive";
          fetch(s, {
            method: 'PUT',
            body: JSON.stringify({
                archived: true
            })
          });
          alert("Message archived");
        }
         
      });
      if(mailbox=="inbox" || mailbox=="archive"){
        master.append(arch);
      }
      
      

      
      if(element.read==false){
        master.style.backgroundColor="white";
      }
      else{
        master.style.backgroundColor="lightGray";
      }
      
      master.style.margin="5px"; 
      master.style.padding="10px";
      master.style.borderRadius="5px";
      master.style.cursor="pointer";
      master.style.display="flex";
      master.style.borderColor="black";
      master.id="master";
      
      if(element.read){
        master.onmouseenter=()=>{
          master.style.backgroundColor="gray";
         }
      
      master.onmouseleave=()=>{
        master.style.backgroundColor="lightGray";
      }
    }
      child.append(master);
      
  });
}

function read_mail(id){

  var s="/emails/".concat(id);
   
   
     
  fetch(s)
  .then(response => response.json())
  .then(email => {
      // Print email
       display_mail(email);
    
      // ... do something else with email ...
  });

}



function display_mail(mail){
  
  document.querySelector("#emails-view").style.display="none";
  document.querySelector('#mail-view').style.display = 'block';
  var title=document.querySelector("#mail-view").querySelector(".title");

  var s='/emails/'.concat(mail.id);
  fetch(s, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  });
  console.log(mail.body);
  title.querySelector(".from").innerHTML=`${mail.sender}`;
  title.querySelector(".to").innerHTML=`${mail.recipients}`;
  title.querySelector(".to").innerHTML=`${mail.recipients}`;
  title.querySelector(".subject").innerHTML=`${mail.subject}`;
  title.querySelector(".time").innerHTML=`${mail.timestamp}`;
  document.querySelector("#mail-view").querySelector(".mail-body").innerHTML=`<pre>${mail.body}</pre>`;

  document.querySelector("#reply").addEventListener("click",()=>{
     compose_email();
      
     document.querySelector('#compose-recipients').value = mail.sender;

     document.querySelector('#compose-recipients').disabled=true;

    document.querySelector('#compose-body').value = `On ${mail.timestamp}, ${mail.sender} wrote: ${mail.body}`;

    document.querySelector('#compose-subject').disabled=true;
        if (mail.subject.search('Re:')) {
          document.querySelector('#compose-subject').value = mail.subject;
        }
        else {
          document.querySelector('#compose-subject').value = `Re: ${mail.subject}`;
        }
       
  });
  

   
}


 