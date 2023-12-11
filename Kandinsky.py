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

# 유형별 반지름의 최소 최대
BIG_CIR_R_MIN, BIG_CIR_R_MAX = 3,5
MID_CIR_R_MIN, MID_CIR_R_MAX = 1.3, 2.5
SML_CIR_R_MIN, SML_CIR_R_MAX = 0.3, 1

# 유형별 원 개수의 최소 최대
BIG_CIR_C_MIN, BIG_CIR_C_MAX = 1,2
MID_CIR_C_MIN, MID_CIR_C_MAX = 5,9
SML_CIR_C_MIN, SML_CIR_C_MAX = 4,8

# 격자 생성 선 개수 최소 최대
LINE_NUM_MIN, LINE_NUM_MAX = 3,6

# 격자 생성 선 길이 최소 최대
LINE_LEN_MIN, LINE_LEN_MAX = 5,10

# Cylinder Radius
CYLINDER_RADIUS=0.15

# SemiCircular
SEMI_CIRCULAR_NAME = 'SemiCircular'
SEMI_CIRCULAR_RADIUS = 0.5
SEMI_CIRCULAR_HEIGHT = 1.0

class CircleType(Enum):
    BIG = 0
    MIDDLE = 1
    SMALL = 2

class Kandinsky:
    def __init__(self):
        # 전체 오브젝트 리스트
        self.allObjects = []

        # 전체 그룹 리스트
        self.allGroup = []

        # 각 타입별로 원 생성
        self.createCircle(CircleType.BIG)
        self.createCircle(CircleType.MIDDLE)
        self.createCircle(CircleType.SMALL)

        # 격자 생성
        self.createCheck()
        
        # 부채꼴 생성
        self.thickness = CYLINDER_RADIUS
        self.height = 1

        num_groups = random.randint(2, 4)

        for i in range(num_groups):
            cylinder_group = self.createSector()

        # 구불선 생성
        num_groups = random.randint(2, 4)

        for i in range(num_groups):
            self.createCurve3D()

        # 연속 반원 3개 생성
        self.createSemiCircular()
    
    def set_random_color(self, object_name):
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

        # 새 머터리얼 생성
        material = cmds.shadingNode('lambert', asShader=True, name=f'{object_name}_Material')
        cmds.setAttr(material + '.color', *random_color, type='double3')

        # 오브젝트에 새 머터리얼 할당
        cmds.select(object_name)
        cmds.hyperShade(assign=material)

        print(f"Color of {object_name} set to: {random_color}")

    #
    # 원 생성
    #
    def createCircle(self, circle_type):

        if circle_type == CircleType.SMALL:
            r_min, r_max = SML_CIR_R_MIN, SML_CIR_R_MAX
            cnt = random.randint(SML_CIR_C_MIN, SML_CIR_C_MAX)
            objectName = 'smallCircle'
            groupName = 'smallCircleGroup'
            smallCircles = []
            circles = smallCircles
        elif circle_type == CircleType.MIDDLE:
            r_min, r_max = MID_CIR_R_MIN, MID_CIR_R_MAX
            cnt = random.randint(MID_CIR_C_MIN, MID_CIR_C_MAX)
            objectName = 'middleCircle'
            groupName = 'middleCircleGroup'
            middleCircles = []
            circles = middleCircles
        elif circle_type == CircleType.BIG:
            r_min, r_max = BIG_CIR_R_MIN, BIG_CIR_R_MAX
            cnt = random.randint(BIG_CIR_C_MIN, BIG_CIR_C_MAX)
            objectName = 'bigCircle'
            groupName = 'bigCircleGroup'
            bigCircles = []
            circles = bigCircles

        for i in range(cnt):
            x = random.uniform(X_MIN, X_MAX)
            y = random.uniform(Y_MIN, Y_MAX)
            z = random.uniform(Z_MIN, Z_MAX)
            
            radius = random.uniform(r_min, r_max)
            circle_name = f'{objectName}{i+1}'
            circle = cmds.polySphere(r=radius,n=circle_name)[0]
            cmds.move(x, y, z, circle)

            self.set_random_color(circle)

            circles.append(circle)

            if(circle_type == CircleType.BIG and radius>3.5):
                sm_radius = random.uniform(MID_CIR_R_MIN, MID_CIR_R_MAX)
                sm_name = f'{objectName}Min'
                sm_circle = cmds.polySphere(r=sm_radius, n=sm_name)[0]
                cmds.move(x, y, z+(radius+sm_radius)/1.5, sm_circle)
                
                self.set_random_color(sm_circle)

                circles.append(sm_circle)
                
                print("sm_radius:", sm_radius, " x:", x, " y:", y, " z:", z)

        group = cmds.group(circles, n=groupName)

        self.allGroup.append(group)
        self.allObjects.append(circles)

        print('groupList: ', self.allGroup)
        print('objectList:', self.allObjects)

        return

    #
    #  격자 생성 함수
    #
    def createCheck(self):
        vertical_x = random.uniform(X_MIN, X_MAX)
        vertical_y = random.uniform(Y_MIN, Y_MAX)
        z = random.uniform(Z_MIN, Z_MAX)

        groupObjects = []
        verticals = []
        horizons = []
        cubes = []

        vertical_cnt = random.randint(LINE_NUM_MIN, LINE_NUM_MAX)
        height = random.uniform(LINE_LEN_MIN, LINE_LEN_MAX)

        name = 'checkVertical'

        for i in range(0, vertical_cnt, 1):
            cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=height, sx=20, sy=1, sz=1, ax=(0, 1, 0), n=f'{name}{i+1}')[0]
            cmds.move(vertical_x+i, vertical_y, z, cylinder)
            verticals.append(cylinder)
            z = random.uniform(Z_MIN, Z_MAX)

            self.set_random_color(cylinder)
        
        self.allObjects.append(verticals)
        groupObjects.extend(verticals)

        horizon_cnt = random.randint(3, 6)
        width = random.uniform(5, 10)
        horizon_x = random.uniform(vertical_x+width/2, vertical_x+vertical_cnt-width/2)
        horizon_y = random.uniform(vertical_y-height/2, vertical_y+height/2-horizon_cnt)

        name = 'checkHorizon'

        for i in range(0, horizon_cnt, 1):
            cylinder = cmds.polyCylinder(r=CYLINDER_RADIUS, h=width, sx=20, sy=1, sz=1, ax=(0, 0, 1), n=f'{name}{i+1}')[0]
            cmds.rotate(0, 90, 0, cylinder)
            cmds.move(horizon_x, horizon_y+i, z, cylinder)
            horizons.append(cylinder)
            z = random.uniform(Z_MIN, Z_MAX)

            self.set_random_color(cylinder)

        self.allObjects.append(horizons)
        groupObjects.extend(horizons)

        name = 'checkCube'

        for i in range(0, vertical_cnt-1):
            for j in range(horizon_cnt,1,-1):
                cube = cmds.polyCube(w=0.7, h=0.7, d=0.7, n=f'{name}{i+1}')[0]
                cmds.move(vertical_x+i+0.5, horizon_y+(horizon_cnt-j)+0.5, z, cube)
                cubes.append(cube)
                z = random.uniform(Z_MIN, Z_MAX)
                self.set_random_color(cube)


                # 색상 설정 추가
            self.set_random_color(cylinder)

        self.allObjects.append(cubes)
        groupObjects.extend(cubes)

        group = cmds.group(groupObjects, n='checkGroup')

         # 랜덤 회전값 생성
        random_rotation_x = random.uniform(-30, 30)
        random_rotation_y = random.uniform(-30, 30)
        random_rotation_z = random.uniform(-30, 30)

        # 그룹에 회전값 적용
        cmds.rotate(random_rotation_x, random_rotation_y, random_rotation_z, group)

        print(self.allObjects)
    
    #
    # 부채꼴 생성 함수
    #
    def createSector(self):
        sectorGroup = cmds.group(em=True)

        cylinder1 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=self.height)[0]
        cmds.move(0, self.height / 2, 0, cylinder1 + ".scalePivot", cylinder1 + ".rotatePivot", absolute=True)
        cylinder2 = cmds.polyCylinder(sx=20, sy=1, sz=1, r=self.thickness, h=self.height)[0]
        cmds.move(0, self.height / 2, 0, cylinder2 + ".scalePivot", cylinder2 + ".rotatePivot", absolute=True)

        scale_y = random.uniform(5, 15)
        cmds.scale(1, scale_y, 1, cylinder1)
        scale_y = random.uniform(5, 15)
        cmds.scale(1, scale_y, 1, cylinder2)

        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, cylinder1, relative=True)
        
        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, cylinder2, relative=True)

        cmds.move(0, 0, 0, [cylinder2 + ".scalePivot", cylinder2 + ".rotatePivot"], absolute=True)
        cmds.move(0, 0, 0, [cylinder2 + ".scalePivot", cylinder2 + ".rotatePivot"], absolute=True)

        cmds.parent(cylinder1, cylinder2, sectorGroup)

        cmds.xform(sectorGroup, pivots=[0, self.height/2, 0], worldSpace=True)

        angle_x = random.uniform(90, 180)
        angle_y = random.uniform(90, 180)
        angle_z = random.uniform(90, 180)
        cmds.rotate(angle_x, angle_y, angle_z, sectorGroup, relative=True)

        x = random.uniform(-15, 15)
        y = random.uniform(0, 30)
        z = random.uniform(-7.5, 7.5)
        cmds.move(x, y, z, sectorGroup, absolute=True)

        self.set_random_color(sectorGroup)

        return sectorGroup  
         
    #
    # 구불구불 선 생성
    #
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
        
        self.set_random_color(cylinder)

    #
    # 연속된 반원 3개 생성
    #
    def createSemiCircular(self):

        group_name = cmds.group(empty=True, name=f'{SEMI_CIRCULAR_NAME}_group')

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

        cmds.parent(combined_result, group_name)

        x_position, y_position, z_position = (random.uniform(-15, 15),random.uniform(0, 30),random.uniform(-7.5, 7.5))
        rotation_values = [random.uniform(0, 360) for _ in range(3)]
        cmds.move(x_position, y_position, z_position, group_name)
        cmds.rotate(*rotation_values, group_name)

        self.set_random_color(group_name)

# Circle 객체 생성
r = Kandinsky()