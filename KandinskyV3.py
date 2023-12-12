import maya.cmds as cmds
import random
import math
from enum import Enum

# 좌표의 최소, 최대
X_MIN, X_MAX = -15,15
Y_MIN, Y_MAX = 0, 30
Z_MIN, Z_MAX = -10, 10

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
            if(self.circleType == CircleType.BIG):
                z = random.uniform(5, 15)
            else:
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
            z = random.uniform(5, 15)

            self.vertical_cnt = random.randint(LINE_NUM_MIN, LINE_NUM_MAX)
            height = random.uniform(LINE_LEN_MIN, LINE_LEN_MAX)

            name = 'checkVertical'

            for i in range(0, self.vertical_cnt, 1):
                cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=height, sx=20, sy=1, sz=1, ax=(0, 1, 0), n=f'{name}{i+1}')[0]
                cmds.move(vertical_x+i, vertical_y, z, cylinder)
                z = random.uniform(5, 15)
                self.objectList.append(cylinder)

            self.horizon_cnt = random.randint(3, 6)
            width = random.uniform(5, 10)
            horizon_x = random.uniform(vertical_x+width/2, vertical_x+self.vertical_cnt-width/2)
            horizon_y = random.uniform(vertical_y-height/2, vertical_y+height/2-self.horizon_cnt)

            name = 'checkHorizon'

            for i in range(0, self.horizon_cnt, 1):
                cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=width, sx=20, sy=1, sz=1, ax=(0, 0, 1), n=f'{name}{i+1}')[0]
                cmds.rotate(0, 90, 0, cylinder)
                cmds.move(horizon_x, horizon_y+i, z, cylinder)
                z = random.uniform(5, 15)
                self.objectList.append(cylinder)

            name = 'checkCube'

            for i in range(0, self.vertical_cnt-1):
                for j in range(self.horizon_cnt,1,-1):
                    cube = cmds.polyCube(w=0.7, h=0.7, d=0.7, n=f'{name}{i+1}')[0]
                    cmds.move(vertical_x+i+0.5, horizon_y+(self.horizon_cnt-j)+0.5, z, cube)
                    z = random.uniform(5, 15)
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
    def __init__(self,num):
        self.thickness = CYLINDER_RADIUS
        self.height = 1
        self.num = num
        self.groupName = 'sectorGroup'

        self.active = False

        self.objectList = []

    def activeTrue(self):
        self.active = True
        self.createSector()
    
    def createSector(self):
        height1 = random.uniform(5, 15)
        height2 = random.uniform(5, 15)

        cylinder1 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=height1, ax=(0, 0, 1))[0]
        cylinder2 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=height2, ax=(0, 0, 1))[0]

        cmds.xform(cylinder1, pivots=[0, 0, height1/2], worldSpace=True)
        cmds.xform(cylinder2, pivots=[0, 0, height2/2], worldSpace=True)

        if height1 < height2:
            cmds.move(0, 0, (height2 - height1)/2, cylinder1)
        else:
            cmds.move(0, 0, (height1 - height2)/2, cylinder2)
        
        angle_y = random.uniform(15, 160)
        cmds.rotate(0, angle_y, 0, cylinder1)

        self.objectList.append(cylinder1)
        self.objectList.append(cylinder2)

        group = cmds.group(self.objectList, n=f'{self.groupName}{self.num}')

        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, group, relative=True)

        x = random.uniform(X_MIN, X_MAX)
        y = random.uniform(Y_MIN, Y_MAX)
        z = random.uniform(Z_MIN, Z_MAX)
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
         
        cylinder = cmds.polyCylinder(r=0.15, h=0.1, sx=20, sy=1, sz=1, ax=(0, 1, 0))[0]

        points_cnt = random.randint(6, 10)
        print('points_cnt',points_cnt)

        maxH = random.uniform(7,15)
        middleH = maxH / 2
        degreeH = middleH
        maxW = maxH+random.uniform(0,5)-2.5
        minW = maxW/(points_cnt*3)

        x = random.uniform(X_MIN, X_MAX)
        y = random.uniform(Y_MIN, Y_MAX)
        z = random.uniform(Z_MIN-maxW/2, Z_MAX+maxW/2)

        cmds.move(x, y, z, cylinder)

        points = []

        for i in range(1,points_cnt+1):
            if(i==1):
                pointX = x
                pointY = y+random.uniform(0,3)
            # i가 홀수인 경우
            elif (i%2==1):
                pointY = y+middleH*(0.5**(points_cnt-(i-1)))-3+random.uniform(0,2)
            # i가 짝수인 경우
            else:
                pointY = y+middleH+middleH*(0.5**(i-1))+random.uniform(-2,0)
            
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

        cmds.move(first_point[0], first_point[1]-0.2, first_point[2], cylinder)

        # 실린더의 한쪽 바닥면 선택 (f[40]부터 f[59]까지)
        faces = ['{0}.f[{1}]'.format(cylinder, i) for i in range(40, 60)]

        # 선택된 페이스들에 대해 추출 실행
        extrude = cmds.polyExtrudeFacet(faces, inputCurve=curve, divisions=maxW*20,ltz=0.1, ltx=0.1, lty=0.1)

        cmds.delete(cylinder, constructionHistory=True)
        cmds.delete(aim_constraint)
        cmds.delete(locator)
        cmds.delete(curve)

        rotateType = random.randint(0, 1)
        if(rotateType==0):
            cmds.rotate(random.uniform(-30,30),random.uniform(-30,30)-180,random.uniform(-30,30), cylinder)
        else:
            cmds.rotate(random.uniform(-30,30),random.uniform(-30,30),random.uniform(-30,30), cylinder)

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
SEMI_CIRCULAR_NAME = 'semiCircular'
SEMI_CIRCULAR_RADIUS = 1.5 
SEMI_CIRCULAR_HEIGHT = 1.5 

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

        group = cmds.group(self.objectList, name=f'{SEMI_CIRCULAR_NAME}Group')

        cmds.delete(combined_result, constructionHistory=True)


        x_position, y_position, z_position = (random.uniform(X_MIN, X_MAX),random.uniform(Y_MIN, Y_MAX),random.uniform(5, 15))
        rotation_values = [random.uniform(0, 360) for _ in range(3)]
        cmds.move(x_position, y_position, z_position, group)
        cmds.rotate(*rotation_values, group)

        self.group = group

    def getGroup(self):
            return self.group
    
    def getObjectList(self):
            return self.objectList

###################################################################

class TetrahedronType(Enum):
    BIG = 0
    MIDDLE = 1
    SMALL = 2

class Tetrahedron:
    def __init__(self,tetrahedronType):
        self.objectList = []
        self.tetrahedronType = tetrahedronType

        self.createTetrahedron()

    def createTetrahedron(self):
        if self.tetrahedronType == TetrahedronType.SMALL:
            d_min, d_max = 0.05, 1
            cnt = random.randint(1, 2)
            objectName = 'smallTetrahedron'
            groupName = 'smallTetrahedronGroup'
        elif self.tetrahedronType == TetrahedronType.MIDDLE:
            d_min, d_max = 1.5, 2.5
            cnt = random.randint(1, 2)
            objectName = 'middleTetrahedron'
            groupName = 'middleTetrahedronGroup'
        elif self.tetrahedronType == TetrahedronType.BIG:
            d_min, d_max = 3, 5
            cnt = 1
            objectName = 'bigTetrahedron'
            groupName = 'bigTetrahedronGroup'

        for i in range(cnt):
            # 무게중심의 랜덤 위치
            center_x = random.uniform(X_MIN,X_MAX)
            center_y = random.uniform(Y_MIN,Y_MAX)
            if(self.tetrahedronType == TetrahedronType.BIG):
                center_z = random.uniform(-5,-15)
            else:
                center_z = random.uniform(Z_MIN,Z_MAX)

            # 무게중심에서 꼭짓점까지의 랜덤 거리
            distance = random.uniform(d_min, d_max)
            edge_length = 2 * distance / math.sqrt(3)

            # 원점에 대한 꼭짓점 좌표
            vertices = [
                (math.sqrt(3)/3 * edge_length, 0, -edge_length/(3*math.sqrt(6))),
                (-math.sqrt(3)/6 * edge_length, edge_length/2, -edge_length/(3*math.sqrt(6))),
                (-math.sqrt(3)/6 * edge_length, -edge_length/2, -edge_length/(3*math.sqrt(6))),
                (0, 0, math.sqrt(6)/3 * edge_length)
            ]

            # 무게중심 위치로 꼭짓점 이동
            vertices_moved = [(x + center_x, y + center_y, z + center_z) for x, y, z in vertices]

            # 각 면을 개별적으로 생성
            faces = []
            faces.append(cmds.polyCreateFacet(p=[vertices_moved[0], vertices_moved[1], vertices_moved[2]])[0])
            faces.append(cmds.polyCreateFacet(p=[vertices_moved[0], vertices_moved[1], vertices_moved[3]])[0])
            faces.append(cmds.polyCreateFacet(p=[vertices_moved[0], vertices_moved[2], vertices_moved[3]])[0])
            faces.append(cmds.polyCreateFacet(p=[vertices_moved[1], vertices_moved[2], vertices_moved[3]])[0])

            # 0번째와 2번째 면을 뒤집음
            cmds.polyNormal(faces[0], normalMode=0, userNormalMode=0, ch=1)
            cmds.polyNormal(faces[2], normalMode=0, userNormalMode=0, ch=1)

            # 생성된 면들을 결합
            tetrahedron = cmds.polyUnite(faces, ch=True, n=f'{objectName}{i}')[0]
            cmds.delete(tetrahedron, ch=True)  # 히스토리 삭제

            cmds.xform(tetrahedron, pivots=[center_x, center_y, center_z], worldSpace=True)

            random_rotation_x = random.uniform(0, 360)
            random_rotation_y = random.uniform(0, 360)
            random_rotation_z = random.uniform(0, 360)
            cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, tetrahedron)

            self.objectList.append(tetrahedron)
            
            cmds.select(clear=True)
        
        group = cmds.group(self.objectList, name=groupName)
        self.group = group

    def getGroup(self):
            return self.group
    
    def getObjectList(self):
            return self.objectList
    
##################################################################

class RandomCube:
    def __init__(self):
        self.groupName = 'randomCubeGroup'
        self.cnt = random.randint(6, 8)

        self.objectList = []
        self.createRandomCube()

    def createRandomCube(self):
        for i in range(self.cnt):

            whd = random.uniform(0.1, 2)

            # 큐브 생성
            cube = cmds.polyCube(w=whd,d=whd,h=whd)[0]

            # 랜덤 위치 생성
            x = random.uniform(X_MIN, X_MAX)
            y = random.uniform(Y_MIN, Y_MAX)
            z = random.uniform(Z_MIN, Z_MAX)

            # 큐브를 랜덤 위치로 이동
            cmds.move(x, y, z, cube)

            # 랜덤 회전값 생성
            rotation_x = random.uniform(0, 360)
            rotation_y = random.uniform(0, 360)
            rotation_z = random.uniform(0, 360)

            # 큐브에 랜덤 회전값 적용
            cmds.rotate(rotation_x, rotation_y, rotation_z, cube)

            self.objectList.append(cube)

        group = cmds.group(self.objectList, n=self.groupName)
        self.group = group

    def getGroup(self):
        return self.group

    def getObjectList(self):
        return self.objectList
###################################################################
class SemiCircleLine():
    def __init__(self):
        self.groupName = 'semiCircleLineGroup'
        self.cnt = random.randint(2, 4)
        self.name = 'semiCircleLine'
        self.num_points=100

        self.objectList = []
        self.createSemiCircleLine()

    def createSemiCircleLine(self):
        for i in range(self.cnt):
            points = []
            
            for i in range(self.num_points):
                x = -SEMI_CIRCULAR_RADIUS + 2 * SEMI_CIRCULAR_RADIUS * float(i) / (self.num_points - 1)
                y = math.sqrt(SEMI_CIRCULAR_RADIUS**2 - x**2)  # 반원 방정식
                points.append((x, y, 0))  # Z 좌표는 0으로 설정

            # 포인트로 커브 생성
            curve = cmds.curve(d=2, p=points)

            # 커브의 첫 번째 포인트에 Locator 생성
            locator = cmds.spaceLocator()[0]
            first_point = cmds.pointPosition(curve + '.cv[0]')
            cmds.move(first_point[0], first_point[1], first_point[2], locator)

            cylinder = cmds.polyCylinder(r=0.15, h=0.1, sx=20, sy=1, sz=1, ax=(0, 1, 0), n=f'{self.name}{i}')[0]

            cmds.move(first_point[0], first_point[1]-0.1, first_point[2], cylinder)

            # 실린더에 Aim Constraint 적용
            # 실린더가 Locator를 바라보도록 설정
            aim_constraint = cmds.aimConstraint(locator, cylinder, aimVector=(0, 1, 0), upVector=(0, 0, 1))

            # 실린더의 한쪽 바닥면 선택 (f[40]부터 f[59]까지)
            faces = ['{0}.f[{1}]'.format(cylinder, i) for i in range(40, 60)]

            # 선택된 페이스들에 대해 추출 실행
            extrude = cmds.polyExtrudeFacet(faces, inputCurve=curve, divisions=80, ltz=0.1, ltx=0.1, lty=0.1)

            cmds.delete(cylinder, constructionHistory=True)
            cmds.delete(aim_constraint)
            cmds.delete(locator)
            cmds.delete(curve)

            # 랜덤 위치 생성
            x = random.uniform(X_MIN, X_MAX)
            y = random.uniform(Y_MIN, Y_MAX)
            z = random.uniform(Z_MIN, Z_MAX)

            # 큐브를 랜덤 위치로 이동
            cmds.move(x, y, z, cylinder)

            # 랜덤 회전값 생성
            rotation_x = random.uniform(0, 360)
            rotation_y = random.uniform(0, 360)
            rotation_z = random.uniform(0, 360)

            # 큐브에 랜덤 회전값 적용
            cmds.rotate(rotation_x, rotation_y, rotation_z, cylinder)

            self.objectList.append(cylinder)

        group = cmds.group(self.objectList, n=self.groupName)
        self.group = group

    def getGroup(self):
        return self.group

    def getObjectList(self):
        return self.objectList
     

##################################################################

def set_random_color(object_name):

    if random.random() < 0.2:
        # 빨간색 계열
        red_component = random.uniform(177, 203)
        green_component = random.uniform(22, 89)
        blue_component = random.uniform(1, 71)
    else:
        # 빨간색 제외
        red_component = random.uniform(62, 250)
        green_component = random.uniform(41, 211)
        blue_component = random.uniform(33, 205)

    random_color = [red_component / 255.0, green_component / 255.0, blue_component / 255.0]

    material = cmds.shadingNode('aiStandardSurface', asShader=True)

    # 매트한 표면 속성 설정
    cmds.setAttr(material + '.specular', 0.1)  # 낮은 반사율
    cmds.setAttr(material + '.specularRoughness', 0.7)  # 높은 거칠기
    cmds.setAttr(material + '.baseColor', *random_color, type='double3') 

    # 새 머터리얼 생성
    # material = cmds.shadingNode('lambert', asShader=True, name=f'{object_name}_Material')
    # cmds.setAttr(material + '.color', *random_color, type='double3')

    # 오브젝트에 새 머터리얼 할당
    cmds.select(object_name)
    cmds.hyperShade(assign=material)

    return material

    # print(f"Color of {object_name} set to: {random_color}")

def set_color_black(object_name):

    color = [37/255.0,31/255.0,35/255.0]
    material = cmds.shadingNode('lambert', asShader=True, name=f'{object_name}_Material')
    cmds.setAttr(material + '.color', *color, type='double3')

    cmds.select(object_name)
    cmds.hyperShade(assign=material)

    return material

####################################################################

def get_slider_value():
    return cmds.intSliderGrp(randomSeedSlider, query=True, value=True)

def Start():
    global allObject, allGroup, materials

    if(activeRandomSeed==True):
        random.seed(get_slider_value())

    print(f'prestart allObject{allObject} allGroup{allGroup}')

    if (len(allObject)>0 or len(allGroup)>0):
        for i in range(len(allGroup)):
            if(cmds.objExists(allGroup[i])):
                    cmds.delete(allGroup[i])

    if(len(materials)>0):
        for i in materials:
            cmds.delete(i)
    
    allObject = []
    allGroup = []
    materials = []

    print('removeMaterials', materials)

    print(f'start allObject{allObject} allGroup{allGroup}')

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

    global sectorCnt

    sectorCnt = random.randint(2, 4)

    sector1 = Sector(1)
    sector2 = Sector(2)
    sector3 = Sector(3)
    sector4 = Sector(4)

    sector1.activeTrue()
    allObject.append(sector1.getObjectList()) 
    allGroup.append(sector1.getGroup())

    sector2.activeTrue()
    allObject.append(sector2.getObjectList()) 
    allGroup.append(sector2.getGroup()) 

    if(sectorCnt>2):
        sector3.activeTrue()
        allObject.append(sector3.getObjectList()) 
        allGroup.append(sector3.getGroup()) 
        if(sectorCnt>3):
            sector4.activeTrue()
            allObject.append(sector4.getObjectList()) 
            allGroup.append(sector4.getGroup())

    global curve3DCnt
    curve3DCnt = random.randint(1, 2)

    curve3D1 = Curve3D(1)
    curve3D2 = Curve3D(2)

    curve3D1.activeTrue()
    allObject.append(curve3D1.getObjectList()) 
    allGroup.append(curve3D1.getGroup()) 

    if(curve3DCnt>1):
        curve3D2.activeTrue()
        allObject.append(curve3D2.getObjectList()) 
        allGroup.append(curve3D2.getGroup()) 

    semiCircular =  SemiCircular()
    allObject.append(semiCircular.getObjectList()) 
    allGroup.append(semiCircular.getGroup()) 

    smallTeltrahedron = Tetrahedron(TetrahedronType.SMALL)
    allObject.append(smallTeltrahedron.getObjectList()) 
    allGroup.append(smallTeltrahedron.getGroup())

    middleTeltrahedron = Tetrahedron(TetrahedronType.MIDDLE)
    allObject.append(middleTeltrahedron.getObjectList()) 
    allGroup.append(middleTeltrahedron.getGroup()) 

    bigTeltrahedron = Tetrahedron(TetrahedronType.BIG)
    allObject.append(bigTeltrahedron.getObjectList()) 
    allGroup.append(bigTeltrahedron.getGroup())

    randomCube = RandomCube()
    allObject.append(randomCube.getObjectList())
    allGroup.append(randomCube.getGroup())

    semiCircleLine = SemiCircleLine()
    allObject.append(semiCircleLine.getObjectList())
    allGroup.append(semiCircleLine.getGroup())

    print('end ', 'allObject :', allObject, 'allGroup :', allGroup)

    global horizon_cnt
    global vertical_cnt

    horizon_cnt = check.horizon_cnt
    vertical_cnt = check.vertical_cnt

    for i in range(len(allGroup)):
        for j in range(len(allObject[i])):
            objectName = f'{allGroup[i]}' + "|" + f'{allObject[i][j]}'
            if(i==3 and j>=0 and j<check.horizon_cnt+check.vertical_cnt):
                materials.append(set_color_black(objectName))
            elif(i>=4 and i<4+sectorCnt):
                materials.append(set_color_black(objectName))
            elif(i>=4+sectorCnt and i<4+sectorCnt+curve3DCnt):
                materials.append(set_color_black(objectName))
            else:
                materials.append(set_random_color(objectName))

    print('materials: ', materials)

    cmds.button(animate_button, edit=True, enable=True)

#######################################################################

def Animation():
    global allObject, allGroup

    for i in range(len(allGroup)):
        if(i==0):
            firstTime = 0
            step = 7
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==1):
            firstTime = 0
            step = 2
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==2):
            firstTime = 0
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==3):
            firstTime = 1
            step = 2
            middleStep = 7
            endStep = 1
            k=0

            horizon = 2
            cube = 4
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)
                
                if(k<vertical_cnt):
                    cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                    firstTime += step
                elif(k<vertical_cnt+horizon_cnt):
                    cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime+horizon)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep+horizon)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep+horizon)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep+horizon)

                    firstTime += step
                else:
                    cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime+cube)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime+cube)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime+cube)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep+cube)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep+cube)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep+cube)

                    cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep+cube)
                    cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep+cube)
                    cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep+cube)

                    firstTime += step

                k += 1
        elif(4<=i<4+sectorCnt):
            firstTime = 2 + 10*(i-4)
            step = 1
            middleStep = 2
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep+4)
        elif(4+sectorCnt<=i<4+sectorCnt+curve3DCnt):
            firstTime = 3 + 10*(i-4)
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt):
            firstTime = 4
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt+1):
            firstTime = 5
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt+2):
            firstTime = 6
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt+3):
            firstTime = 7
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt+4):
            firstTime = 8
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step
        elif(i==4+sectorCnt+curve3DCnt+5):
            firstTime = 9
            step = 4
            middleStep = 7
            endStep = 1
            for j in allObject[i]:
                objectName = f'{allGroup[i]}' + "|" + f'{j}'
                cmds.xform(objectName, centerPivots = True)

                cmds.setKeyframe(objectName, attribute='scaleX', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleY', value=0, time=firstTime)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=0, time=firstTime)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1.1, time=firstTime+middleStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1.1, time=firstTime+middleStep)

                cmds.setKeyframe(objectName, attribute='scaleX', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleY', value=1, time=firstTime+middleStep+endStep)
                cmds.setKeyframe(objectName, attribute='scaleZ', value=1, time=firstTime+middleStep+endStep)

                firstTime += step


########################################################################

global allObject
global allGroup
global activeRandomSeed
global materials
allObject = []
allGroup = []
materials = []
activeRandomSeed = False

def toggle_slider(*args):
    # 체크박스 상태에 따라 슬라이더 활성화 또는 비활성화
    checked = cmds.checkBox(randomSeedCheckBox, query=True, value=True)
    cmds.intSliderGrp(randomSeedSlider, edit=True, enable=checked)
    global activeRandomSeed
    activeRandomSeed= checked

# UI 창이 이미 열려있다면 닫기
if cmds.window("Kandinsky", exists=True):
    cmds.deleteUI("Kandinsky")

# UI 창 생성
my_window = cmds.window("Kandinsky", title="Kandinsky",w=100, h=200, sizeable=False)

# 레이아웃 생성
cmds.columnLayout(adjustableColumn=True)
cmds.separator(height=10)
cmds.text(label="Make Modeling", align='center', font='boldLabelFont')  # 제목 스타일 텍스트
cmds.separator(height=10)
cmds.separator(height=5, style='none')

# 랜덤 시드 사용 여부를 선택하는 체크박스
randomSeedCheckBox = cmds.checkBox(label="Use Random Seed", value=False, changeCommand=toggle_slider)

# 랜덤 시드를 설정하는 슬라이더 (기본적으로 비활성화 상태)
randomSeedSlider = cmds.intSliderGrp(label='Random Seed', min=0, max=100, value=1, step=1,f=True, enable=False)

# 버튼 추가
cmds.button(label="make", command="Start()")

cmds.separator(height=15, style='none')

cmds.separator(height=10)
cmds.text(label="Make Animation", align='center', font='boldLabelFont')  # 제목 스타일 텍스트
cmds.separator(height=10)
cmds.separator(height=10, style='none')

animate_button = cmds.button(label="Animate", command="Animation()", enable=False)

# UI 창 표시
cmds.showWindow(my_window)