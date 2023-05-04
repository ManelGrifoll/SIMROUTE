%clear all,clc,close all

%%%%% START INPUT FILES
%%% load SIMROUTE results
file='TESTCASE_LIV_ALI.mat';
file2='out/TESTCASE_LIV_ALI_fix.mat';

nom_resul2='TESTCASE_emissions';

EL=0.80;%Engine load (in unit percentage)% 
Pow_Ins=55440;%Engine Power(kW)
V_design=27;%Velocity design (knots)
SFOC=175; %Specific fuel compsuntion (gr/kWh). 
SC=0.005; %Sulphur content of fuel (mass%) for Fuel Oil - IMO 2020 outside ECA zones
CC=0.88; %Carbon content of fuel (mass %) MDO
Engine_RPM=514; % Engine rpm; 

M_S=32.0655; %Molar mass of sulphur (gr/mol)
M_SO2=64.06436; % molar mass of sulphur dioxide g/mol (number of mols of S=number of mols of SO2)
M_C=12.01; %Molar mass of carbon (gr/mol)
M_CO2=44.0886; %Molar mass of carbon dioxide (gr/mol) (number of mols of C=number of mols of CO2)


%%PARTICULATE MATTER%

EF_EC=0.08; %Emission factor elementary carbon (gr/kWh)
EF_OC=0.2; % Emission factor for organic carbon (gr/kWh)
EF_ASH=0.06; %Emission factor for ash (gr/kWh)
OC_EL=1.024; %Part of organic carbon dependent of EL (dimensionless)


%%%%% END INPUT FILES

%%%%
SIM=load(file);
SIM_fix=load(file2);

cte_k=(EL*Pow_Ins)/((V_design)^3);%Constant K (kW/kn^3)

Pow_trans_h=cte_k*(SIM.vt).^3; % transient Power at each interval (kW) (interval = node to node)
Pow_trans_h_fix=cte_k*(SIM_fix.vt_fix).^3; % hourly transient Power (kW)

Pow_trans=sum(Pow_trans_h(1:end))/(length(Pow_trans_h));% Average Transient Power Opt
Pow_trans_fix=sum(Pow_trans_h_fix(1:end))/(length(Pow_trans_h_fix));%Average Transitient Power Dmin

Delta_V=SIM.v0-SIM.vt; % speed loss due to waves


%%%%%%%% RUTA OPTIMA %%%%%%%%%%%%%%

Pow_Ef=Pow_Ins*0.80; % Effective power
Delta_Pow=Pow_trans_h.*(1./((1-(Delta_V/SIM.v0)).^3)-1); % Power increase to maintain speed
Pow_New=Pow_Ef+Delta_Pow(2:end);

%figure (1)

%plot(SIM.costt(2:end),Pow_New);
%xlabel('Hours')
%ylabel('Total power needed to maintain speed')
%grid on

%%Impact of enigne load EL on SFOC

EL_New=Pow_New/Pow_Ins;

%%% In literature, it is assumed to have a linear relation between fuel consumption and EL,
%%% and SFOC is assumed to be constant. Taking a look to manufacturers data, we see that SFOC is a non-linear
%%% function of EL. Looking at manufacturers data, it can be seen that there
%%% is an apporximately parabolic dependency between them. STEAM 2 assumes a parabolic function for all engines. 
%%% Using regression analysis from engine manufacturers data, STEAM 2 gets the equation for SFOCrel 

SFOC_REL_New=(0.445*(EL_New.^2))-(0.71*EL_New)+1.28; 

%%% And the absolute fuel consumption is estimated from:

SFOC_End=SFOC_REL_New*SFOC;

Interv_t=diff(SIM.costt); % Time interval between nodes (if there are 100 nodes, there will be 99 intervals)

Fuel_comp_New=Pow_New.*SFOC_End.*Interv_t; % in gr

Fuel_comp_End=sum(Fuel_comp_New(1:end));

disp(['Fuel Consumption optimized route: ' num2str(Fuel_comp_End/.10^(-06)) ' Tn'])


%%%%%%%% RUTA MÍNIMA %%%%%%%%%%%%%%
Delta_V_fix=SIM.v0-SIM_fix.vt_fix;
Delta_Pow_fix=Pow_trans_h_fix.*(1./((1-(Delta_V_fix/SIM.v0)).^3)-1); % Power increase to maintain speed
Pow_New_fix=Pow_Ef+Delta_Pow_fix(2:end);
EL_New_fix=Pow_New_fix/Pow_Ins;
SFOC_REL_New_fix=(0.445*(EL_New_fix.^2))-(0.71*EL_New_fix)+1.28;
SFOC_End_fix=SFOC_REL_New_fix*SFOC;

Interv_t_fix=diff(SIM_fix.cost_fix); 

Fuel_comp_New_fix=Pow_New_fix.*SFOC_End_fix.*Interv_t_fix; % in gr
Fuel_comp_End_fix=sum(Fuel_comp_New_fix(1:end));

disp(['Fuel Consumption minimum route: ' num2str(Fuel_comp_End_fix/.10^(-06)) ' Tn'])

Fuel_saving=(1-(Fuel_comp_End/Fuel_comp_End_fix))*100;

disp(['Fuel consumption reduction following optimum route: ' num2str(Fuel_saving) ' %'])


%figure (4)

%plot(SIM_fix.cost_fix(2:end),Pow_New_fix);
%xlabel('Hours')
%ylabel('Total power needed to maintain speed (Dmin)')
%grid on

%%%%%%%% RUTA OPTIMA %%%%%%%%%%%%%%

%%% SO2
n_SO2_Interv=(SFOC_End*SC)/M_S;% number of mols of sulphur dioxide (mol/kWh)
Emi_fac_SO2_Interv=M_SO2*n_SO2_Interv; % SO2 Emission factor (gr/kWh)

SO2_Interv=Pow_New.*EL_New.*Emi_fac_SO2_Interv.*Interv_t; % SO2 emited at each interval in (gr)

SO2_End=sum(SO2_Interv(1:end)); % Accumulated SO2 for the whole trip in (gr)

%%% CO2
n_CO2_Interv=(SFOC_End*CC)/M_C;% number of mols of carbon dioxide (mol/kWh)
Emi_fac_CO2_Interv=M_CO2*n_CO2_Interv; % CO2 Emission factor (gr/kWh)

CO2_Interv=Pow_New.*EL_New.*Emi_fac_CO2_Interv.*Interv_t; % CO2 emited at each interval in (gr)

CO2_End=sum(CO2_Interv(1:end));

%%% NOX
%NOx emission factor gr/kWh

if Engine_RPM<130;
    Emi_fac_NOx=17;
else
    if (130<=Engine_RPM)&&(Engine_RPM<=2000);
        Emi_fac_NOx=45*Engine_RPM^(-0.2);
    else
        if Engine_RPM>2000;
            Emi_fac_NOx=9.8;
        end
    end
    
end


NOx_Interv=Pow_New.*EL_New.*Emi_fac_NOx.*Interv_t; % NOx emited at each interval in (gr)

NOx_End=sum(NOx_Interv(1:end)); %Accumulated NOx emited optimized route (gr)

%%% PARTICULATE MATTER

EF_SO4=0.312*SC; % Emission factor for SO4 (gr/kWh)
EF_H2O=0.244*SC; % Emission factor H2O (gr/kWh)

Emi_fac_PM_Interv=SFOC_REL_New*(EF_SO4+EF_H2O+EF_OC*OC_EL+EF_EC+EF_ASH); %Particulate matter emission factor (gr/kWh)

PM_Interv=Pow_New.*EL_New.*Emi_fac_PM_Interv.*Interv_t; %PM emited at each interval in (gr)

PM_End=sum(PM_Interv(1:end)); % Accumulated PM emited optimized route (gr)



%%%%%%%% RUTA MÍNIMA %%%%%%%%%%%%%%

%%% SO2
n_SO2_Interv_fix=(SFOC_End_fix*SC)/M_S;% number of mols of sulphur dioxide (mol/kWh)
Emi_fac_SO2_Interv_fix=M_SO2*n_SO2_Interv_fix; % SO2 Emission factor (gr/kWh)

SO2_Interv_fix=Pow_New_fix.*EL_New_fix.*Emi_fac_SO2_Interv_fix.*Interv_t_fix; % SO2 emited at each interval in (gr)

SO2_End_fix=sum(SO2_Interv_fix(1:end)); % Accumulated SO2 for the whole minimum distance trip in (gr)


%%% CO2
n_CO2_Interv_fix=(SFOC_End_fix*CC)/M_C;% number of mols of carbon dioxide (mol/kwh)
Emi_fac_CO2_Interv_fix=M_CO2*n_CO2_Interv_fix; % CO2 Emission factor (gr/kWh)

CO2_Interv_fix=Pow_New_fix.*EL_New_fix.*Emi_fac_CO2_Interv_fix.*Interv_t_fix; %CO2 emited at each interval in (gr)

CO2_End_fix=sum(CO2_Interv_fix(1:end)); % Accumulated CO2 for the whole minimum distance trip in (gr)


%%% NOX
%NOx emission factor (gr/kWh)

if Engine_RPM<130;
    Emi_fac_NOx=17;
else
    if (130<=Engine_RPM)&&(Engine_RPM<=2000);
        Emi_fac_NOx=45*Engine_RPM^(-0.2);
    else
        if Engine_RPM>2000;
            Emi_fac_NOx=9.8;
        end
    end
    
end


NOx_Interv_fix=Pow_New_fix.*EL_New_fix.*Emi_fac_NOx.*Interv_t_fix; % NOx emited per interval in (gr)

NOx_End_fix=sum(NOx_Interv_fix(1:end)); % Accumulated NOx for the whole minimum distance route (gr)


%%% PARTICULATE MATTER

EF_SO4=0.312*SC; % Emission factor for SO4 (gr/kWh)
EF_H2O=0.244*SC; % Emission factor H2O (gr/kWh)

Emi_fac_PM_Interv_fix=SFOC_REL_New_fix*(EF_SO4+EF_H2O+EF_OC*OC_EL+EF_EC+EF_ASH); %Particulate matter emission factor (gr/kWh)

PM_Interv_fix=Pow_New_fix.*EL_New_fix.*Emi_fac_PM_Interv_fix.*Interv_t_fix; %PM emited per interval in (gr)

PM_End_fix=sum(PM_Interv_fix(1:end)); % Accumulated PM per minimum distance route in (gr)

Emissions_mitigation_percentage=(1-(CO2_End/CO2_End_fix))*100;

disp(['Percentage of emissions mitigation following optimum route: ' num2str(Emissions_mitigation_percentage) ' %'])

disp(['CO2 optimized: ' num2str(CO2_End/.10^(-06)) ' Tn'])
disp(['CO2 minimum: ' num2str(CO2_End_fix/.10^(-06)) ' Tn'])
disp(['SO2 optimized: ' num2str(SO2_End/.10^(-06)) ' Tn'])
disp(['SO2 minimum: ' num2str(SO2_End_fix/.10^(-06)) ' Tn'])
disp(['NOx optimized: ' num2str(NOx_End/.10^(-06)) ' Tn'])
disp(['NOx minimum: ' num2str(NOx_End_fix/.10^(-06)) ' Tn'])
disp(['PM optimized: ' num2str(PM_End/.10^(-06)) ' Tn'])
disp(['PM minimum: ' num2str(PM_End_fix/.10^(-06)) ' Tn'])
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

figure(2)

subplot(2,2,1);
plot(SIM.costt(2:end),CO2_Interv/.10^(-06),'r',SIM_fix.cost_fix(2:end),CO2_Interv_fix/.10^(-06),'--r')
title('Minimum vs Optimum route CO2 emissions / t interval')
grid on
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('CO2 opt','CO2 min')

subplot(2,2,2);
plot(SIM.costt(2:end),NOx_Interv/.10^(-06),'k',SIM_fix.cost_fix(2:end),NOx_Interv_fix/.10^(-06),'--k')
title('Minimum vs Optimum route NOx emissions / t interval')
grid on
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('NOx opt','NOx min')

subplot(2,2,3);
plot(SIM.costt(2:end),SO2_Interv/.10^(-06),'b',SIM_fix.cost_fix(2:end),SO2_Interv_fix/.10^(-06),'--b')
title('Minimum vs Optimum route SO2 emission / t interval')
grid on
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('SO2 opt','SO2 min')

subplot(2,2,4);
plot(SIM.costt(2:end),PM_Interv/.10^(-06),'g',SIM_fix.cost_fix(2:end),PM_Interv_fix/.10^(-06),'--g')
title('Minimum vs Optimum route PM emission / t interval')
grid on
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('PM opt','PM min')

saveas(gcf,'Min Route vs Opt Route Emissions.jpg')

figure(3)

subplot(2,2,1)
plot(SIM.costt(2:end),cumsum(CO2_Interv/.10^(-06)),'o r',SIM_fix.cost_fix(2:end),cumsum(CO2_Interv_fix/.10^(-06)),'+r')
grid on
title('CO_2 accumulated/trip')
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('CO2 opt','CO2 min')

subplot(2,2,2)
plot(SIM.costt(2:end),cumsum(NOx_Interv/.10^(-06)),'o k',SIM_fix.cost_fix(2:end),cumsum(NOx_Interv_fix/.10^(-06)),'+k')
grid on
title('NO_x accumulated/trip')
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('NOx opt','NOx min')
subplot(2,2,3)
plot(SIM.costt(2:end),cumsum(SO2_Interv/.10^(-06)),'o b',SIM_fix.cost_fix(2:end),cumsum(SO2_Interv_fix/.10^(-06)),'+b')
grid on
title('SO_2 accumulated/trip')
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('SO2 opt','SO2 min')

subplot(2,2,4)
plot(SIM.costt(2:end),cumsum(PM_Interv/.10^(-06)),'o g',SIM_fix.cost_fix(2:end),cumsum(PM_Interv_fix/.10^(-06)),'+g')
grid on
title('PM accumulated/trip')
xlabel('Hours')
ylabel('Emissions (Tn)')
legend('PM opt','PM min')

saveas(gcf,'Accumulated Emissions.jpg')

%legend('SO2 opt','NOx opt','PM opt','SO2 min','NOx min','PM min');

save(['out/' nom_resul2])

