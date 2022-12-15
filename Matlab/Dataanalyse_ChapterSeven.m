clear
clc

csvfiles = dir('Weld/*.csv'); %Folder for P_data
Nfiles =4;% length(csvfiles); 

SD_P_data=readmatrix('MigaLogchapter7');
FindZero=find(SD_P_data(:,1)==0);

A(:,1)=["Experiment:";"MC";"MV";"MW";"MG";"SR";"SD_MC";"SD_MV";"SD_MW";"SD_MG"; "DC";"DV";"DW";"DG"];
P_Time=(1:Nfiles);
for i = 1:Nfiles
% P_data %
filename= csvfiles(i).name;
P_data=readmatrix(fullfile('Weld/',filename));
M_voltage=median(P_data(:,3))./10;
M_Current=median(P_data(:,2))./10;
M_Wire=median(P_data(:,4))./10;
M_Gas=median(P_data(:,5))./10;

% SD_P_data %     
    if i==2
        B=SD_P_data(FindZero(i)+1:(FindZero(i+1)-1),:);
    elseif i<Nfiles-1    
        B=SD_P_data(FindZero(i):(FindZero(i+1)-1),:);
    else
        B=SD_P_data(FindZero(i):length(SD_P_data),:);
    end
    C=find(isnan(B), 1, 'first');
    SD_data=B(1:C-1,:);
M_voltage_SD=median(SD_data(:,1));
M_Current_SD=median(SD_data(:,2));
M_Wire_SD=median(SD_data(:,3));
M_Gas_SD=median(SD_data(:,4));
F=length(P_data);
SampleRate=F./((P_data(F,1)-P_data(1,1))*0.001);

P_Time(i)=(P_data(F,1)-P_data(1,1))*0.001;

% Deviation %
DC=abs(((M_Current-M_Current_SD)./M_Current_SD)*100);
DV=abs(((M_voltage-M_voltage_SD)./M_voltage_SD)*100);
DW=abs(((M_Wire-M_Wire_SD)./M_Wire_SD)*100);
DG=abs((M_Gas-M_Gas_SD)./M_Gas_SD)*100;

% All in one %
P_data=[i;M_Current;M_voltage;M_Wire;M_Gas;SampleRate;M_Current_SD;M_voltage_SD;M_Wire_SD;M_Gas_SD;DC;DV;DW;DG];
A(:,i+1)=P_data;

end
