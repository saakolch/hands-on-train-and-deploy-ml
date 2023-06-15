from pydantic import BaseModel
import pickle
from comet_ml import API

from sklearn.pipeline import Pipeline

from src.logger import get_console_logger

logger = get_console_logger('deployer')

try:
    # this code works when running on Cerebrium
    from cerebrium import get_secret
    COMET_ML_API_KEY = get_secret("COMET_ML_API_KEY")
except ImportError:
    # this code works when running locally
    import os
    COMET_ML_API_KEY = os.environ['COMET_ML_API_KEY']

def load_model_from_registry() -> Pipeline:
    """Loads the model from the remote model registry"""

    api = API(api_key=COMET_ML_API_KEY)

    # find model version to deploy
    model = api.get_model(workspace='paulescu', model_name='linear-model')
    try:
        model_version = model.find_versions(status='production')[0]
    except IndexError as e:
        logger.error('No production version found for model')
        raise e
    
    # download model from comet ml registry to local file
    api.download_registry_model(
        workspace="paulescu",
        registry_name="linear-model",
        version=model_version,
        # stage='production',
        output_path='./',
        expand=True
    )
    
    # load model from local file to memory
    with open('./model.pkl', "rb") as f:
        model = pickle.load(f)
    
    return model

model = load_model_from_registry()

class Item(BaseModel):
    price_24_hour_ago: float
    price_23_hour_ago: float
    price_22_hour_ago: float
    price_21_hour_ago: float
    price_20_hour_ago: float
    price_19_hour_ago: float
    price_18_hour_ago: float
    price_17_hour_ago: float
    price_16_hour_ago: float
    price_15_hour_ago: float
    price_14_hour_ago: float
    price_13_hour_ago: float
    price_12_hour_ago: float
    price_11_hour_ago: float
    price_10_hour_ago: float
    price_9_hour_ago: float
    price_8_hour_ago: float
    price_7_hour_ago: float
    price_6_hour_ago: float
    price_5_hour_ago: float
    price_4_hour_ago: float
    price_3_hour_ago: float
    price_2_hour_ago: float
    price_1_hour_ago: float

def predict(item, run_id, logger):
    item = Item(**item)

    # transform item to dataframe
    import pandas as pd
    df = pd.DataFrame([item.dict()])

    # predict
    prediction = model.predict(df)[0]

    return {"prediction": prediction}

if __name__ == '__main__':
    item = {
        'price_24_hour_ago': 46656.851562,
        'price_23_hour_ago': 46700.535156,
        'price_22_hour_ago': 46700.535156,
        'price_21_hour_ago': 46700.535156,
        'price_20_hour_ago': 46700.535156,
        'price_19_hour_ago': 46700.535156,
        'price_18_hour_ago': 46700.535156,
        'price_17_hour_ago': 46700.535156,
        'price_16_hour_ago': 46700.535156,
        'price_15_hour_ago': 46700.535156,
        'price_14_hour_ago': 46700.535156,
        'price_13_hour_ago': 46700.535156,
        'price_12_hour_ago': 46700.535156,
        'price_11_hour_ago': 46700.535156,
        'price_10_hour_ago': 46700.535156,
        'price_9_hour_ago': 46700.535156,
        'price_8_hour_ago': 46700.535156,
        'price_7_hour_ago': 46700.535156,
        'price_6_hour_ago': 46700.535156,
        'price_5_hour_ago': 46700.535156,
        'price_4_hour_ago': 46700.535156,
        'price_3_hour_ago': 46700.535156,
        'price_2_hour_ago': 46700.535156,
        'price_1_hour_ago': 46700.535156
    }

    prediction = predict(item, None, None)
    print(f'{prediction=}')