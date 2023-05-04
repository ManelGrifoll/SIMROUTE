function  d=dist_nods(N1,N2)
global nodes;
lon1=nodes(N1,1);
lat1=nodes(N1,2);
lon2=nodes(N2,1);
lat2=nodes(N2,2);
d=60*(acosd(sind(lat1)*sind(lat2)+cosd(lat1)*cosd(lat2)*cosd(lon1-lon2)));