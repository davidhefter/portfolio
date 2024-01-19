function dx = pendcart_StateSpace(x,m,M,L,g,d,u)

% m     % pend mass
% M     % cart mass
% L     % pend length
% g     % gravity
% d     % Friction force
% u     % external force comes from the controller
y = x;
m1=M;
m2=m;
r=L;
x=y(1,1);
xd=y(2,1);
th=y(3,1);
thd=y(4,1);
sth=sin(th);
cth=cos(th);
F=u-d*xd;

dx(1,1) = xd;
dx(2,1) = -((m2*g*sin(th)*cos(th)) + (m2*r*(thd^2)*sin(th)) + F)/((m2*(cos(th)^2))-(m1+m2));
dx(3,1) = thd;
dx(4,1) = (((m1+m2)*g*sin(th))+((m2*r*(thd^2)*sin(th))+F)*cos(th))/(r*((m2*(cos(th)^2))-(m1+m2)));