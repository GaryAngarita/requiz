console.log('hello world')
const timer=document.getElementById('displaytimer')
console.log(timer.textContent)
const inputtag = document.getElementById('timer')

t=0
setInterval(()=>{
t+=1
timer.innerHTML ="<b>Timer: " +t+" seconds</b>"
inputtag.value = t
},1000)