'''This is the program to generate training data for the main program.'''
import math
import os
import subprocess
import sys
import lifelib
import dataman
#Set to store octohashes:
octodigests = set()
#The data. Yes.
data = []
#Set up the lifetree:
if len(sys.argv) > 1:
    rule = sys.argv[1]
else:
    rule = input('Enter a rule.\n>')
rule = rule.replace('/', '').lower()
try:
    sess = lifelib.load_rules(rule)
except:
    print('Rule '+rule+' not valid, defaulting to b3s23...')
    sess = lifelib.load_rules('b3s23')
lt = sess.lifetree(n_layers = 1, memory = 1000)
#Time for my favourite part of functional programming: creating a giant pile of functions
#that will collapse as soon as one thing goes wrong.
def bash(command):
    '''Runs a bash command, using the same bash lifelib uses.'''
    local_bash = lifelib.autocompile.get_local_bash()
    parsed = command.split(' ')
    cmd = local_bash + parsed
    proc = subprocess.Popen(cmd, stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    output = proc.communicate()
    return output
def generatecollisions(numgliders):
    '''Gets a list of 100000 glider collisions.'''
    if not os.path.isfile(os.getcwd() + '/shipcolls'):
        #Compile shipcolls if the file does not exist.
        import setup
    bashcmd = bash(os.getcwd() + '''/shipcolls -g bob$bbo$ooo! -r b3s23 -n '''+str(numgliders)+''' -t 100000''')
    collisions = bashcmd[0].decode('utf-8').split('\n')
    return collisions    
def getgcount(pt):
    '''Gets the number of gliders in a pattern.'''
    gliders = 0
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            gliders = gliders + 1
    return gliders
def getgliderset(pt):
    '''Gets just the gliders of a pattern.'''
    #Useful for determining validity, as well as rewinding.

    gliders = lt.pattern('b!')
    components = pt.components()
    for x in components:
        if x.wechsler in ['153', '163']:
            gliders = gliders + x
    return gliders
def rewind(pt, amount):
    '''Rewinds gliders in a pattern by a given number of generations.'''
    components = pt.components()
    shift = math.ceil(amount/4)
    for x in components:
        if x.wechsler in ['153', '163']:
            pt = pt - x
            displacement = x.displacement
            x = x(displacement[0] * -1 * shift, displacement[1] * -1 * shift)
            if amount%4 != 0:
                x = x[4-(amount%4)]
            pt = pt + x
    return pt
def isvalid(pt):
    '''Determines if a synthesis is valid or not.'''
    gliders = getgliderset(pt)
    return rewind(gliders, 500)[500].digest() == gliders.digest()
def advance(pt):
    '''Advances a synthesis until 3 generations before the number of gliders decreases.'''
    #A basic binary search is employed to do this.
    pt = rewind(pt, 4) #Rewind the pattern to ensure we can advance it.
    glidercount = getgcount(pt)
    if glidercount == 0:
        return pt
    gens = 1
    while getgcount(pt[gens]) == glidercount:
        gens = gens * 2
    gap = gens//4
    gens = gens - gap
    while gap > 1:
        evpt = pt[gens]
        gap = gap//2
        if getgcount(evpt) == glidercount:
            gens = gens + gap
        else:
            gens = gens - gap
    return pt[gens - 3]
def isvalid(pt):
    '''Determines if a collision is valid.'''
    comp = pt.components()
    for x in comp:
        if x.wechsler not in ['153', '163']:
            return False
    return rewind(pt, 4)[4] == pt
def striprle(rle):
    '''Strips an rle down into a cleaner format.'''
    for _ in range(2):
        rle = rle[rle.find('\n')+1:]
    rle = rle.replace('\n', '')
    return rle
def process(rle):
    '''Processes a collision.'''
    pt = lt.pattern(rle)
    if not isvalid(pt):
       return None
    pt = advance(pt)
    octodigest = pt.octodigest()
    if octodigest in octodigests:
        return None
    evpt = pt[200]
    if evpt[2] != evpt or evpt.empty():
        return None
    apgcode = evpt.apgcode
    octodigests.add(octodigest)
    orientations = [pt, pt("rot270"), pt("rot180"), pt("rot90"), pt("flip_x"), pt("flip_y"), pt("swap_xy"), pt("swap_xy_flip")]
    
    json_data = {'apgcode':apgcode,'octodigest':octodigest}
    for x in range(8):
        json_data['orient' + str(x) + 'digest'] = orientations[x].digest()
        json_data['orient' + str(x) +'rle'] = striprle(orientations[x].rle_string())
    data.append(json_data)
process('''x = 9, y = 3, rule = B3/S23
bo5bo$2bo3bo$3o3b3o!
''')
process('''x = 9, y = 3, rule = B3/S23
bo5bo$2bo3bo$3o3b3o!
''')
print(data)

