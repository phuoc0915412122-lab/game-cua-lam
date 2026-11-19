with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

anim_char3 = '''  3: {
    idle: {frames:[{src:"characters/3/idle_01.png",ms:240},{src:"characters/3/idle_02.png",ms:240}],loop:true,width:64,height:72,offsetY:6},
    move: {frames:[{src:"characters/3/move_01.png",ms:95},{src:"characters/3/move_02.png",ms:95},{src:"characters/3/move_03.png",ms:95},{src:"characters/3/move_04.png",ms:95}],loop:true,width:64,height:72,offsetY:6},
    jump: {frames:[{src:"characters/3/jump_01.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    fall: {frames:[{src:"characters/3/fall_01.png",ms:160}],loop:true,width:64,height:72,offsetY:6,flip:false},
    attack: {frames:[{src:"characters/3/attack_01.png",ms:75},{src:"characters/3/attack_02.png",ms:75},{src:"characters/3/attack_03.png",ms:110}],loop:false,width:64,height:72,offsetY:6},
    skill: {frames:[{src:"characters/3/skill_01.png",ms:110},{src:"characters/3/skill_02.png",ms:100},{src:"characters/3/skill_03.png",ms:140}],loop:false,width:64,height:72,offsetY:6},
    finisher: {frames:[{src:"characters/3/finisher_01.png",ms:110},{src:"characters/3/finisher_02.png",ms:90},{src:"characters/3/finisher_03.png",ms:160}],loop:false,width:64,height:72,offsetY:6},
    dash: {frames:[{src:"characters/3/dash_01.png",ms:70},{src:"characters/3/dash_02.png",ms:70}],loop:true,width:64,height:72,offsetY:6},
    defeat: {frames:[{src:"characters/3/defeat_01.png",ms:200}],loop:false,width:64,height:72,offsetY:6,flip:false}
  },'''

target = ' characters: {\n  0: {'
replacement = ' characters: {\n' + anim_char3 + '\n  0: {'

if target in text:
    text = text.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully added character 3 animations to index.html!')
else:
    print('Target not found!')
