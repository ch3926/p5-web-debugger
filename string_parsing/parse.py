import re
import random
import string

def generate_random_string(length=100):
    """
    Generate a random string of a given length.
    
    Args:
    length (int): Length of the random string to be generated. Default is 100.
    
    Returns:
    str: A random string of the specified length.
    """
    # Using a combination of lowercase, uppercase letters, digits, and punctuation
    characters = string.ascii_letters
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

def read_js_file(file_path):
    with open(file_path, 'r') as file:
        return file.readlines()
    
def handle_global_line(line: str) -> list[str]:
    '''
    split at ; and = \n
    
    createCanvas -> var dfsdfsdf = createCanvas()
    var.parent('canvas-container')

    "everything the starts w/ create but the following"

    exclude createVector(), createShader(), createFilterShader(), createCamera()
    - maybe just match the ones
    '''

    inits = [a.strip() for a in line.split(";")]
    inits = [i for i in inits if i != '']

    ## break it up into declarations
    p5_assigments = []
    global_declarations = []

    

    for init in inits:
        components = init.split(" ")
        if components[0] == 'const':   ## ignore const
            init += ";"
            global_declarations.append(init)
            continue
        assignment = "" + " ".join(components[1:])
        assignment += ";"
        declaration = "" + " ".join(components[:2])
        declaration += ";"
        p5_assigments.append(assignment)
        global_declarations.append(declaration)
    
    return p5_assigments, global_declarations


def transform_code(lines, keyword_re, global_re):
    '''
    code composed of 3 parts \n
    global_vars - track through paren stack \n
    other_funcs \n
    setup()
    '''

    key_pattern = re.compile(keyword_re)
    global_pattern = re.compile(global_re)


    ## function stacks
    setup_braces = []
    global_braces = []

    ## setup stuff
    in_setup = False
    p5_setup = []
    setup = []

    ## only declaring for scope
    p5_assigments = []
    global_declarations = []

    ## output
    output_content = []
    hold_code = []


    for line in lines:
        code_line: str = line.split("//")[0]

        if "function setup()" in code_line or "function setup " in code_line:
            ## handle function declaration
            in_setup = True
            new_code = code_line.replace("setup()", "p5_setup()")
            if "{" in code_line:
                setup_braces.append("{")
            setup.append(line)
            p5_setup.append(new_code)
            continue
        
        if "function draw()" in code_line or "function draw " in code_line:
            ## change - no continue statement
            code_line = code_line.replace("draw()", "p5_draw()")

        if in_setup:
            ## handle setup() vs p5_setup() function
            if "{" in code_line:
                setup_braces.append("{")
            
            if "}" in code_line:
                setup_braces.pop()
            
            ## partition keywords vs setup
            if key_pattern.search(code_line):   # is not None?
                a = key_pattern.search(code_line).group()
                b = generate_random_string(10)

                setup.append(f"\tvar {b} = {a}\n")
                setup.append(f"\t{b}.parent('canvas-container');\n")
            else:
                p5_setup.append(line)
            
            if not setup_braces:
                setup.append("}\n")

                in_setup = False
        else:
            ## handle other functions and global code
            if "{" in code_line:
                global_braces.append("{")

            if "}" in code_line:
                global_braces.pop()
            
            if not global_braces and global_pattern.match(code_line):
                local_p5, local_global_decs = handle_global_line(code_line) 
                p5_assigments.extend(local_p5)
                global_declarations.extend(local_global_decs)
            else:
                ## other code
                hold_code.append(code_line)


    for assignment in p5_assigments:
        p5_setup.insert(1, "\t" + assignment + "\n")


    for declaration in global_declarations:
        output_content.append(declaration + "\n")

    output_content.append("\n")
    output_content.extend(setup)
    output_content.append("\n")
    output_content.extend(p5_setup)
    output_content.extend(hold_code)
    
    return output_content









def write_js_file(file_path, lines):
    with open(file_path, 'w') as file:
        for line in lines:
            file.write(line)



global_pattern = "(let)|(var)|(const)"     # match const, handle later
key_pattern = '(createDiv|createP|createSpan|createImg|createA|createSlider|createButton|createCheckbox|createSelect|createRadio|createColorPicker|createInput|createFileInput|createVideo|createAudio|createCapture|createElement|createWriter|createImage|createCanvas|createGraphics|createFramebuffer)(.*)'


original_file_path = 'text.js'
transformed_file_path = 'output.js'

lines = read_js_file(original_file_path)
transformed_lines = transform_code(lines, key_pattern, global_pattern)
write_js_file(transformed_file_path, transformed_lines)