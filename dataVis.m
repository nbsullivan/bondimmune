% DATAVIS - Visualize cleaned data over time.
%
% 21 November 2016
close all;

irate = csvread('trimmed_data.csv',1,3);
figure(1)
set(gcf,'Position',[669 185 560 420])
[T,D] = meshgrid([1,3,6,12*[1,2,3,5,7,10,20,30]],1:2812);
surf(T,D,irate); shading flat
colormap('gray')
xlabel('term (months)'); ylabel('day id'); zlabel('rate')

figure(2)
set(gcf,'Position',[87 183 560 420])
for i = 1:5:2812
    figure(2)
    plot([1,3,6,12*[1,2,3,5,7,10,20,30]],irate(i,:),'r.-')
    axis([0 12*30 0 6])
    title(['Day id: ' num2str(i)])
    xlabel('term (months)'); ylabel('rate')
    pause(.01)
end