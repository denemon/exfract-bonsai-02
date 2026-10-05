// Portrait views are composed in 3D, with a more oblique view of the broad crown.
export function viewFor(width,height){
 const aspect=width/height,portrait=height>width;
 if(portrait){
  const narrow=Math.max(0,Math.min(1,(.462-aspect)/.119));
  const azimuth=(55+17*narrow)*Math.PI/180,distance=5.35+.35*narrow;
  return {position:[Math.sin(azimuth)*distance,1.45,Math.cos(azimuth)*distance],target:[.075,.94,-.065],fov:43,portrait:true};
 }
 return {position:[1.85,1.50,3.85],target:[.05,.91,-.12],fov:38.5,portrait:false};
}
