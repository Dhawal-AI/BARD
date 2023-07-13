from flask import Flask, render_template, request
from bardapi import Bard
import pandas as pd

app = Flask(__name__)

# Set up the PICOS criteria and Bard API token
picos_criteria = {
    'Population': ['psoriasis', 'intertriginous psoriasis', 'scalp psoriasis', 'plaque psoriasis',
                   'nail psoriasis', 'pustular psoriasis', 'erythrodermic psoriasis', 'guttate psoriasis'],
    'Intervention': ['anti tumor necrosis factor', 'tnf', 'tnf-alpha inhibitor',
                     'adalimumab', 'etanercept', 'infliximab', 'certolizumab pegol', 'golimumab',
                     'anti-interleukin 12', 'anti-il12', 'ustekinumab', 'anti-interleukin 17', 'anti-il17',
                     'secukinumab', 'ixekizumab', 'brodalumab', 'bimekizumab', 'anti-interleukin 23',
                     'anti-il-23', 'guselkumab', 'tildrakizumab', 'risankizumab', 'mirikizumab', 't-cell inhibitor',
                     'abatacept'],
    'Comparison': ['Topical agents', 'Vitamin D', 'Calcitriol', 'Salicylic Acid', 'Calcipotriol', 'Calcipotriene',
                   'Tacalcitol', 'Dovonex', 'Dovobet', 'Curatoderm', 'Tazarotene', 'Zorac', 'Silkis', 'Maxacalcitol',
                   'Corticosteroid', 'Steroid', 'Hydrocortisone', 'Betamethasone', 'Beclometasone', 'Clobetasol',
                   'Fluocinonide', 'Fluocortolone', 'Hydrocortisone', 'Mometasone', 'Desoximetasone', 'Alclometasone',
                   'Amcinonide', 'Diflucortolone', 'Flurandrenolide', 'Fludroxycortide', 'Ultralanum',
                   'Flurandrenolone', 'Diflorasone', 'Halcinonide', 'Triamcinolone', 'Clocortolone', 'Fluocinolone',
                   'Halobetasol', 'Elocon', 'Adcortyl', 'Aureocort', 'Haelan', 'Fluticasone Propionate', 'Cutivate',
                   'Synalar', 'Fluocinonide', 'Metosyn', 'Betacap', 'Betnovate', 'Diprosone', 'Hydrocortisyl',
                   'Mildison', 'Alphaderm', 'Calmurid', 'Coal Tar', 'Dithranol', 'Oxacalcitriol', 'Anthralin',
                   'Psorigel', 'Balneum', 'Polytar', 'Tarcortin', 'Dithranol', 'Dithrocream', 'Exorex', 'Ionil',
                   'Meted', 'Etretin', 'Tacrolimus', 'Cyclosporin', 'Retinoid', 'Methotrexate', 'Acitretin',
                   'Neotigason', 'Ciclosporin', 'Macrolactam', 'Pimecrolimus', 'Anti-Tumor Necrosis Factor', 'TNF',
                   'TNF-Alpha Inhibitor', 'Adalimumab', 'Etanercept', 'Infliximab', 'Certolizumab Pegol', 'Golimumab',
                   'Anti-Interleukin 12', 'Anti-IL12', 'Ustekinumab', 'Anti-Interleukin 17', 'Anti-IL17', 'Secukinumab',
                   'Ixekizumab', 'Brodalumab', 'Bimekizumab', 'Anti-Interleukin 23', 'Anti-IL-23', 'Guselkumab',
                   'Tildrakizumab', 'Risankizumab', 'Mirikizumab', 'T-Cell Inhibitor', 'Abatacept'],
    'Outcome': ['PASI 100 response rate', 'PASI 90 response rate', 'PASI 75 response rate', 'PGA 0/1', 'sPGA 0/1',
                'IGA 0/1', 'DLQI improvement'],
    'Study_design': ['Randomized controlled trials']
}

# Initialize Bard API
bard_token = 'Xwj5sVDzqYsdp-biewkbpM26kz7DmFI1KENySgrFflnFoGaD3SnrP6EMvUYTYOpuWI4qkw.'
bard = Bard(token=bard_token)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/review', methods=['POST'])
def review():
    csv_file = request.files['csv_file']
    df = pd.read_csv(csv_file, encoding='latin-1', on_bad_lines='skip')

    iterations = len(df)
    results = []

    for i in range(1):
        title = df['Title'][i]
        abstract = df['Abstract'][i]
        message = generate_program(picos_criteria, title, abstract)
        response = bard.get_answer(message)
        result = response['content']
        results.append(result)

    return render_template('results.html', results=results)

