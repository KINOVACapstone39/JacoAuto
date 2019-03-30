clear all
close all
clc

%% Kiwi Point Cloud import
Kiwi = pcread('KiwiCloud.ply'); %import from file
r = 0.5; %cube of interest range (meters)
roi = [-r r;-r r;-r r];
indices = findPointsInROI(Kiwi, roi);
Kiwi_s = select(Kiwi,indices); %create cropped cloud
gridStep = 0.01;
Kiwi_s = pcdownsample(Kiwi_s,'gridAverage',gridStep);
% pcshow(Kiwi_s,'MarkerSize',150) %show cloud
% pc.MarkerSize = 10;

% findNeighborsInRadius(Kiwi_s,Kiwi_s.Location(1,:),0.01);
threshold = 0.03;
n = size(Kiwi_s.Location,1);
l = 1;
group = zeros(1,4);
list = [1:n]'*[1 0];

for i = 1:n
%     if (list(i,2))
%         %if i has already been used, skip to next i
%         nexti();
%     else
        %update i status to used
%         list(i,2) = 1;
        %find nearest neighbour and distance
        [indices,dists] = findNearestNeighbors(Kiwi_s,Kiwi_s.Location(i,:),2);
        if (dists(2)>=threshold) %if distance is below threshhold create new group number
            l = l+1;
        end
        %make next i the nearest neighbour we just found
        
        %assign next neighbour to temp
        temp = [Kiwi_s.Location(indices(2),:),l];
        %concatenate group with temp
        group = [group;temp];
    end
    
% end
group(1,:) = [];

c = colormap(lines(l));
cmap = zeros(1,3);

for i = 1:size(group,1)
    cmap = [cmap;c(group(i,4),:)];
end
cmap(1,:) = [];
cmap = floor(255*cmap);
C = uint8(cmap);

Kiwi_s.Color = C;
% 
pcshow(Kiwi_s,'MarkerSize',150) %show cloud



