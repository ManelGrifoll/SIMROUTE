function l=dist_trip(trip)
% Function that searches the distance travelled by trip in milles
n=length(trip);
l=0;
for i=n:-1:2
    l=l+dist_nods(trip(i),trip(i-1));
end
    
    