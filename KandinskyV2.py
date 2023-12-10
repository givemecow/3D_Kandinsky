import maya.cmds as cmds
import random
from enum import Enum

# 초기화
cmds.select(all=True)
cmds.delete()

# 좌표의 최소, 최대
X_MIN, X_MAX = -15,15
Y_MIN, Y_MAX = 0, 30
Z_MIN, Z_MAX = -7.5, 7.5

#############################################################

# 유형별 반지름의 최소 최대
BIG_CIR_R_MIN, BIG_CIR_R_MAX = 3,5
MID_CIR_R_MIN, MID_CIR_R_MAX = 1.3, 2.5
SML_CIR_R_MIN, SML_CIR_R_MAX = 0.3, 1

# 유형별 원 개수의 최소 최대
BIG_CIR_C_MIN, BIG_CIR_C_MAX = 1,2
MID_CIR_C_MIN, MID_CIR_C_MAX = 5,9
SML_CIR_C_MIN, SML_CIR_C_MAX = 4,8

class CircleType(Enum):
    BIG = 0
    MIDDLE = 1
    SMALL = 2


class Circle:
    def __init__(self, circleType):
        self.circleType = circleType
        self.objectList = []
        self.createCircle()

    def createCircle(self):

        if self.circleType == CircleType.SMALL:
            r_min, r_max = SML_CIR_R_MIN, SML_CIR_R_MAX
            cnt = random.randint(SML_CIR_C_MIN, SML_CIR_C_MAX)
            objectName = 'smallCircle'
            groupName = 'smallCircleGroup'
            smallCircles = []
        elif self.circleType == CircleType.MIDDLE:
            r_min, r_max = MID_CIR_R_MIN, MID_CIR_R_MAX
            cnt = random.randint(MID_CIR_C_MIN, MID_CIR_C_MAX)
            objectName = 'middleCircle'
            groupName = 'middleCircleGroup'
            middleCircles = []
        elif self.circleType == CircleType.BIG:
            r_min, r_max = BIG_CIR_R_MIN, BIG_CIR_R_MAX
            cnt = random.randint(BIG_CIR_C_MIN, BIG_CIR_C_MAX)
            objectName = 'bigCircle'
            groupName = 'bigCircleGroup'
            bigCircles = []

        for i in range(cnt):
            x = random.uniform(X_MIN, X_MAX)
            y = random.uniform(Y_MIN, Y_MAX)
            z = random.uniform(Z_MIN, Z_MAX)
            
            radius = random.uniform(r_min, r_max)
            circle_name = f'{objectName}{i+1}'
            circle = cmds.polySphere(r=radius,n=circle_name)[0]
            cmds.move(x, y, z, circle)

            self.objectList.append(circle)

            if(self.circleType == CircleType.BIG and radius>3.5):
                sm_radius = random.uniform(MID_CIR_R_MIN, MID_CIR_R_MAX)
                sm_name = f'{objectName}Min'
                sm_circle = cmds.polySphere(r=sm_radius, n=sm_name)[0]
                cmds.move(x, y, z+(radius+sm_radius)/1.5, sm_circle)
                
                self.objectList.append(sm_circle)
                
                print("sm_radius:", sm_radius, " x:", x, " y:", y, " z:", z)

        self.group = cmds.group(self.objectList, n=groupName)
    
    def getGroup(self):
        return self.group
    
    def getObjectList(self):
        return self.objectList
#####################################################################

# 격자 생성 선 개수 최소 최대
LINE_NUM_MIN, LINE_NUM_MAX = 3,6

# 격자 생성 선 길이 최소 최대
LINE_LEN_MIN, LINE_LEN_MAX = 5,10

# Cylinder Radius
CYLINDER_RADIUS=0.15

class Check:
        def __init__(self):
            self.objectList = []
            self.createCheck()
        
        def createCheck(self):
            vertical_x = random.uniform(X_MIN, X_MAX)
            vertical_y = random.uniform(Y_MIN, Y_MAX)
            z = random.uniform(Z_MIN, Z_MAX)

            vertical_cnt = random.randint(LINE_NUM_MIN, LINE_NUM_MAX)
            height = random.uniform(LINE_LEN_MIN, LINE_LEN_MAX)

            name = 'checkVertical'

            for i in range(0, vertical_cnt, 1):
                cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=height, sx=20, sy=1, sz=1, ax=(0, 1, 0), n=f'{name}{i+1}')[0]
                cmds.move(vertical_x+i, vertical_y, z, cylinder)
                z = random.uniform(Z_MIN, Z_MAX)
                self.objectList.append(cylinder)

            horizon_cnt = random.randint(3, 6)
            width = random.uniform(5, 10)
            horizon_x = random.uniform(vertical_x+width/2, vertical_x+vertical_cnt-width/2)
            horizon_y = random.uniform(vertical_y-height/2, vertical_y+height/2-horizon_cnt)

            name = 'checkHorizon'

            for i in range(0, horizon_cnt, 1):
                cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=width, sx=20, sy=1, sz=1, ax=(0, 0, 1), n=f'{name}{i+1}')[0]
                cmds.rotate(0, 90, 0, cylinder)
                cmds.move(horizon_x, horizon_y+i, z, cylinder)
                z = random.uniform(Z_MIN, Z_MAX)
                self.objectList.append(cylinder)

            name = 'checkCube'

            for i in range(0, vertical_cnt-1):
                for j in range(horizon_cnt,1,-1):
                    cube = cmds.polyCube(w=0.7, h=0.7, d=0.7, n=f'{name}{i+1}')[0]
                    cmds.move(vertical_x+i+0.5, horizon_y+(horizon_cnt-j)+0.5, z, cube)
                    z = random.uniform(Z_MIN, Z_MAX)
                    self.objectList.append(cube)

            group = cmds.group(self.objectList, n='checkGroup')

            # 랜덤 회전값 생성
            random_rotation_x = random.uniform(-30, 30)
            random_rotation_y = random.uniform(-30, 30)
            random_rotation_z = random.uniform(-30, 30)

            # 그룹에 회전값 적용
            cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, group)

            self.group = group

        def getGroup(self):
            return self.group
    
        def getObjectList(self):
            return self.objectList
        
#################################################################

class Sector:
    def __init__(self):
        self.thickness = CYLINDER_RADIUS
        self.height = 1
        self.groupName = 'semiCircularGroup'

        self.active = False

        self.objectList = []

    def activeTrue(self):
        self.active = True
        self.createSector()
    
    def createSector(self):

        cylinder1 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=self.height)[0]
        cmds.move(0, self.height / 2, 0, cylinder1 + ".scalePivot", cylinder1 + ".rotatePivot", absolute=True)
        scale_y = random.uniform(5, 15)
        cmds.scale(1, scale_y, 1, cylinder1)
        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, cylinder1, relative=True)
        cmds.move(0, 0, 0, [cylinder1 + ".scalePivot", cylinder1 + ".rotatePivot"], absolute=True)
        self.objectList.append(cylinder1)

        cylinder2 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=self.height)[0]
        cmds.move(0, self.height / 2, 0, cylinder2 + ".scalePivot", cylinder2 + ".rotatePivot", absolute=True)
        scale_y = random.uniform(5, 15)
        cmds.scale(1, scale_y, 1, cylinder2)
        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, cylinder2, relative=True)
        cmds.move(0, 0, 0, [cylinder2 + ".scalePivot", cylinder2 + ".rotatePivot"], absolute=True)
        self.objectList.append(cylinder2)

        
        group = cmds.group(self.objectList, n=self.groupName)

        cmds.xform(group, pivots=[0, self.height/2, 0], worldSpace=True)

        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, group, relative=True)

        x = random.uniform(-15, 15)
        y = random.uniform(0, 30)
        z = random.uniform(-7.5, 7.5)
        cmds.move(x, y, z, group, absolute=True)

        self.group = group

    def getGroup(self):
            return self.group
    
    def getObjectList(self):
            return self.objectList

###################################################################

class Curve3D:
    def __init__(self,align):
        self.active = False
        self.align = align

        self.objectList = []
    
    def activeTrue(self):
        self.active = True
        self.createCurve3D()

    def createCurve3D(self):
         
        cylinder = cmds.polyCylinder(r=0.2, h=0.1, sx=20, sy=1, sz=1, ax=(0, 1, 0))[0]

        x = random.uniform(X_MIN, X_MAX)
        y = random.uniform(Y_MIN, Y_MAX)
        z = random.uniform(Z_MIN, Z_MAX)

        cmds.move(x, y, z, cylinder)

        points_cnt = random.randint(6, 10)
        print('points_cnt',points_cnt)

        maxH = random.uniform(7,15)
        middleH = maxH / 2
        degreeH = middleH
        maxW = maxH+random.uniform(0,5)-2.5
        minW = maxW/(points_cnt*3)
        points = []

        for i in range(1,points_cnt+1):
            if(i==1):
                pointX = x
                pointY = y
            # i가 홀수인 경우
            elif (i%2==1):
                pointY = y+middleH/(points_cnt-(i-1))-3
            # i가 짝수인 경우
            else:
                pointY = y+middleH+middleH/(i-1)
            
            points.append((pointX, pointY, z))

            pointX = pointX+i*minW
 
        print(points)

        degree = 3

        knots = [0] * degree + list(range(1, points_cnt - degree)) + [points_cnt - degree] * degree

        print(knots)

        curve = cmds.curve(d=degree, p=points, k=knots)

        # 커브의 첫 번째 포인트에 Locator 생성
        locator = cmds.spaceLocator()[0]
        first_point = cmds.pointPosition(curve + '.cv[0]')
        cmds.move(first_point[0], first_point[1], first_point[2], locator)

        # 실린더에 Aim Constraint 적용
        # 실린더가 Locator를 바라보도록 설정
        aim_constraint = cmds.aimConstraint(locator, cylinder, aimVector=(0, 1, 0), upVector=(0, 0, 1))

        cmds.move(x-0.4, y-0.4, z, cylinder)

        # 실린더의 한쪽 바닥면 선택 (f[40]부터 f[59]까지)
        faces = ['{0}.f[{1}]'.format(cylinder, i) for i in range(40, 60)]

        # 선택된 페이스들에 대해 추출 실행
        extrude = cmds.polyExtrudeFacet(faces, inputCurve=curve, divisions=50, ltz=0.5)

        cmds.delete(cylinder, constructionHistory=True)
        cmds.delete(aim_constraint)
        cmds.delete(locator)
        cmds.delete(curve)

        self.objectList.append(cylinder)
        groupName = 'curve3D'
        group = cmds.group(self.objectList, n=f'{groupName}{self.align}')
        self.group = group

    def getGroup(self):
            return self.group
    
    def getObjectList(self):
            return self.objectList
    
###################################################################

# SemiCircular
SEMI_CIRCULAR_NAME = 'SemiCircular'
SEMI_CIRCULAR_RADIUS = 0.5
SEMI_CIRCULAR_HEIGHT = 1.0

class SemiCircular:
    def __init__(self):
        self.objectList = []
        self.createSemiCircular()

    def createSemiCircular(self):

        column_name = cmds.polyCylinder(name=SEMI_CIRCULAR_NAME, radius=SEMI_CIRCULAR_RADIUS, height=SEMI_CIRCULAR_HEIGHT, sx=20, sy=1, sz=1, axis=(0, 1, 0))[0]

        cube_name = cmds.polyCube(name=f'{SEMI_CIRCULAR_NAME}_cube', width=SEMI_CIRCULAR_RADIUS * 8, height=SEMI_CIRCULAR_HEIGHT * 2, depth=SEMI_CIRCULAR_RADIUS * 2)[0]
        cmds.move(0, 0, SEMI_CIRCULAR_RADIUS, cube_name)
        cmds.scale(SEMI_CIRCULAR_RADIUS * 2.0 / SEMI_CIRCULAR_RADIUS, 1.0, 1.0, cube_name)

        result_name = cmds.polyBoolOp(column_name, cube_name, operation=2, name=f'{SEMI_CIRCULAR_NAME}_result')[0]
        
        cmds.polyExtrudeFacet(result_name + '.f[0]', ltz=SEMI_CIRCULAR_HEIGHT/12)
        cmds.scale(4, 1, 1, result_name + '.f[0]')

        duplicates = []
        for i in range(1, 4):
            copy_name = cmds.duplicate(result_name, name=f'{SEMI_CIRCULAR_NAME}_{i}')[0]
            cmds.move(i * (SEMI_CIRCULAR_RADIUS * 2), 0, 0, copy_name, absolute=True)
            duplicates.append(copy_name)

        combined_result = cmds.polyUnite([result_name] + duplicates, name=f'{SEMI_CIRCULAR_NAME}_combined')[0]
        self.objectList.append(combined_result)

        group = cmds.group(self.objectList, name=f'{SEMI_CIRCULAR_NAME}_group')

        x_position, y_position, z_position = (random.uniform(-15, 15),random.uniform(0, 30),random.uniform(-7.5, 7.5))
        rotation_values = [random.uniform(0, 360) for _ in range(3)]
        cmds.move(x_position, y_position, z_position, group)
        cmds.rotate(*rotation_values, group)
        
        cmds.delete(combined_result, constructionHistory=True)
        cmds.delete(column_name)
        cmds.delete(cube_name)
        cmds.delete(result_name)
        for i in range(1, 4):
             cmds.delete(duplicates[i])

        self.group = group

    def getGroup(self):
            return self.group
    
    def getObjectList(self):
            return self.objectList
    
##################################################################

allObject = []
allGroup = []

bigCircle = Circle(CircleType.BIG)
allObject.append(bigCircle.getObjectList()) 
allGroup.append(bigCircle.getGroup()) 

middleCircle = Circle(CircleType.MIDDLE)
allObject.append(middleCircle.getObjectList())
allGroup.append(middleCircle.getGroup())

smallCircle = Circle(CircleType.SMALL)
allObject.append(smallCircle.getObjectList()) 
allGroup.append(smallCircle.getGroup()) 


check = Check()
allObject.append(check.getObjectList())  
allGroup.append(check.getGroup())  


semiCircularCnt = random.randint(2, 4)

semiCircular1 = Sector()
semiCircular2 = Sector()
semiCircular3 = Sector()
semiCircular4 = Sector()

semiCircular1.activeTrue()
allObject.append(semiCircular1.getObjectList()) 
allGroup.append(semiCircular1.getGroup())

semiCircular2.activeTrue()
allObject.append(semiCircular2.getObjectList()) 
allGroup.append(semiCircular2.getGroup()) 

if(semiCircularCnt>2):
    semiCircular3.activeTrue()
    allObject.append(semiCircular3.getObjectList()) 
    allGroup.append(semiCircular3.getGroup()) 
    if(semiCircularCnt>3):
        semiCircular4.activeTrue()
        allObject.append(semiCircular4.getObjectList()) 
        allGroup.append(semiCircular4.getGroup()) 

curve3DCnt = random.randint(2, 4)

curve3D1 = Curve3D(1)
curve3D2 = Curve3D(2)
curve3D3 = Curve3D(3)
curve3D4 = Curve3D(4)

curve3D1.activeTrue()
allObject.append(curve3D1.getObjectList()) 
allGroup.append(curve3D1.getGroup())

curve3D2.activeTrue()
allObject.append(curve3D2.getObjectList()) 
allGroup.append(curve3D2.getGroup()) 

if(curve3DCnt>2):
    curve3D3.activeTrue()
    allObject.append(curve3D3.getObjectList()) 
    allGroup.append(curve3D3.getGroup()) 
    if(curve3DCnt>3):
        curve3D4.activeTrue()
        allObject.append(curve3D4.getObjectList()) 
        allGroup.append(curve3D4.getGroup()) 

semiCircular =  SemiCircular()
allObject.append(semiCircular.getObjectList()) 
allGroup.append(semiCircular.getGroup()) 

print(allObject)
print(allGroup)