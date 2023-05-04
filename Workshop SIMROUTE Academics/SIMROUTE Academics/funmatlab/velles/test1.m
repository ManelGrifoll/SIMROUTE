l_nods=[17591,22970,25897,22194,26741,18400,20685,22176 , 25283, 18217,25904,22380,20506 ];
l_time=[4.005,7.880];
[a,nnods]=size(l_nods);
[a,ttime]=size(l_time);
file_13=fopen('out/test.dat','w');
for t=1:ttime    
    for n=1:nnods
        l_fills=veins(l_nods(n));
        [a,ffills]=size(l_fills);
        for f=1:ffills;
            a=time_edge(v0, l_nods(n), l_fills(f), l_time(t));
            fprintf(file_13,'%5d %5d %10.5f %10.5f\n', l_nods(n), l_fills(f), l_time(t),a);
                              
         end
    end
             
end
fclose(file_13);