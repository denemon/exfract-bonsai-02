export function viewFor(width,height){
 const portrait=height>width;
 if(portrait){const scale=Math.max(1,(390/844)/(width/height));return {position:[5.18*scale,2.70,5.72*scale],target:[.12,1.40,-.05],fov:52,portrait:true};}
 return {position:[3.15,2.55,5.7],target:[0,1.24,-.15],fov:42,portrait:false};
}
