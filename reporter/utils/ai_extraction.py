import base64
import json
import os
from typing import Optional

from openai import OpenAI, OpenAIError

with open('/etc/ai.json') as config_file:
    config = json.load(config_file)

##### REMEMBER TO STORE AS VARIABLE
client = OpenAI(
  api_key=config['api'],
)
###########################################################################


def _encode_image_to_data_url(path: str) -> str:
    """
    Encode an image file to a base64 data URL usable by OpenAI vision models.
    """
    ext = os.path.splitext(path)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        mime = "image/jpeg"
    elif ext == ".png":
        mime = "image/png"
    else:
        # default; you can expand this if needed
        mime = "image/jpeg"

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    return f"data:{mime};base64,{b64}"


def extract_ai_fields_from_images(
    front_image_path: Optional[str],
    back_image_path: Optional[str] = None,
) -> dict:
    """
    Send one or two label images to OpenAI and get back the ai_* fields
    as structured JSON.

    Returns a dict you can directly assign to:
      ai_payload, ai_brand, ai_product_name, ai_product_type,
      ai_abv, ai_milliliters, ai_fl_oz, ai_warning_label, ai_warning_text
    """

    # Build the message content for the model
    contents = [
        {
            "type": "text",
            "text": (
                "You are an expert at reading alcohol product labels. "
                "You will receive one or two images of the same product "
                "(front and possibly back label).\n\n"
                "Extract the following fields and return ONLY a JSON object "
                "with these EXACT keys (no extra text):\n"
                "  ai_brand (string),\n"
                "  ai_product_name (string),\n"
                "  ai_product_type (string; free text like [Must choose most accurate match to following: Beer, Wine, Liquor, Liqueur, Cider, Mead, Sake, Hard Seltzer, Kombucha, Beer - Lager, Beer - Pilsner, Beer - Helles, Beer - Dunkel, Beer - Bock, Beer - Doppelbock, Beer - Märzen / Oktoberfest, Beer - Vienna Lager, Beer - Pale Ale, Beer - Amber Ale, Beer - Brown Ale, Beer - India Pale Ale (IPA), Beer - Double IPA, Beer - Triple IPA, Beer - Hazy / New England IPA, Beer - West Coast IPA, Beer - Stout, Beer - Milk Stout, Beer - Imperial Stout, Beer - Porter, Beer - Wheat Beer, Beer - Hefeweizen, Beer - Belgian Witbier, Beer - Belgian Ale, Beer - Saison, Beer - Farmhouse Ale, Beer - Sour Beer, Beer - Gose, Beer - Lambic, Beer - Berliner Weisse, Beer - Barleywine, Beer - Scotch Ale, Wine - Red Wine, Wine - White Wine, Wine - Rosé, Wine - Sparkling Wine, Wine - Dessert Wine, Wine - Fortified Wine, Wine - Cabernet Sauvignon, Wine - Merlot, Wine - Pinot Noir, Wine - Syrah / Shiraz, Wine - Malbec, Wine - Zinfandel, Wine - Sangiovese, Wine - Nebbiolo, Wine - Tempranillo, Wine - Grenache, Wine - Barbera, Wine - Carménère, Wine - Petit Verdot, Wine - Mourvèdre, Wine - Chardonnay, Wine - Sauvignon Blanc, Wine - Pinot Grigio / Pinot Gris, Wine - Riesling, Wine - Moscato, Wine - Chenin Blanc, Wine - Viognier, Wine - Gewürztraminer, Wine - Sémillon, Wine - Grüner Veltliner, Wine - Albariño, Wine - Champagne, Wine - Prosecco, Wine - Cava, Wine - Port, Wine - Sherry, Wine - Madeira, Wine - Marsala, Wine - Ice Wine, Liquor - Vodka, Liquor - Whiskey, Liquor - Bourbon, Liquor - Rye Whiskey, Liquor - Scotch, Liquor - Irish Whiskey, Liquor - Japanese Whisky, Liquor - Canadian Whisky, Liquor - Rum, Liquor - White Rum, Liquor - Dark Rum, Liquor - Spiced Rum, Liquor - Gin, Liquor - London Dry Gin, Liquor - Tequila, Liquor - Blanco Tequila, Liquor - Reposado Tequila, Liquor - Añejo Tequila, Liquor - Mezcal, Liquor - Brandy, Liquor - Cognac, Liquor - Armagnac, Liquor - Calvados, Liquor - Grappa, Liquor - Aquavit, Liquor - Absinthe, Liqueur - Coffee Liqueur, Liqueur - Cream Liqueur, Liqueur - Orange Liqueur, Liqueur - Herbal Liqueur, Liqueur - Amaro, Liqueur - Anise Liqueur, Liqueur - Fruit Liqueur]),\n"
                "  ai_abv (integer percentage, e.g., 13, or null if unknown),\n"
                "  ai_milliliters (floating point number of bottle size in mL, or null if unknown),\n"
                "  ai_fl_oz (floating point number of fluid ounces, or null if unknown),\n"
                "  ai_warning_label (boolean, true if a legal/health warning appears),\n"
                "  ai_warning_text (string verbatim of the warning text; empty string if none).\n\n"
                "  ai_readable (boolean),\n"
                "  ai_error (string).\n\n"



                "IMPORTANT RULES:\n"
                "If a value is not clearly present, set it to null (for numbers) "
                "or an empty string (for text), and false for ai_warning_label.\n\n"
                "- If the image is blurry, out of focus, very dark/bright, or does not clearly show an alcohol label "
                "  that you can read, you MUST set ai_readable to false, set ai_error to a short reason, and leave:\n"
                "    ai_brand, ai_product_name, ai_product_type, ai_warning_text as empty strings,\n"
                "    ai_abv, ai_milliliters, ai_fl_oz as null,\n"
                "    ai_warning_label as false.\n"
                "- Do NOT guess or hallucinate a brand, product name, type, volume, or ABV when the label text "
                "  is not clearly legible.\n"
                "- Labels may show volume in milliliters (mL), liters (L), or fluid ounces (fl oz).\n"
                "- If the label shows liters (L), you MUST convert to milliliters using 1 liter = 1000 milliliters.\n"
                "- If both mL and fl oz are present on the label, use the label values as-is."
            ),
        }
    ]

    if front_image_path:
        contents.append(
            {
                "type": "image_url",
                "image_url": {"url": _encode_image_to_data_url(front_image_path)},
            }
        )

    if back_image_path:
        contents.append(
            {
                "type": "image_url",
                "image_url": {"url": _encode_image_to_data_url(back_image_path)},
            }
        )

    # Safe defaults so your app doesn't blow up on errors
    default_data = {
        "ai_brand": "",
        "ai_product_name": "",
        "ai_product_type": "",
        "ai_abv": None,
        "ai_milliliters": None,
        "ai_fl_oz": None,
        "ai_warning_label": False,
        "ai_warning_text": "",
        "ai_readable": False,
        "ai_error": "",
    }

    if not front_image_path and not back_image_path:
        return {
            "ai_payload": json.dumps({"error": "no_images_provided"}),
            **default_data,
        }

    try:
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",  # or another vision-capable model
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You extract structured data from product label images."},
                {"role": "user", "content": contents},
            ],
        )

        content = completion.choices[0].message.content
        parsed = json.loads(content)


        # Ensure keys exist early
        for k, v in default_data.items():
            parsed.setdefault(k, v)

        # 🚫 Only bail out if the model explicitly says unreadable
        if parsed.get("ai_readable") is False:
            error_message = parsed.get("ai_error") or "unreadable_image"
            return {
                "ai_payload": json.dumps(
                    {
                        "raw_response": parsed,
                        "error": error_message,
                    }
                ),
                **default_data,
                "ai_error": error_message,  # override default ""
            }

        parsed = _compute_volumes_from_raw(parsed) ## Fix fluid  conversion and rounding



    except (OpenAIError, json.JSONDecodeError, KeyError, IndexError) as exc:
        # Log exc if you have logging configured
        return {
            "ai_payload": json.dumps({"error": str(exc)}),
            **default_data,
        }

    # Ensure all expected keys exist; if not, fill with defaults
    for k, v in default_data.items():
        parsed.setdefault(k, v)

    # Build the dict that matches your model fields
    return {
        "ai_payload": json.dumps(
            {
                "raw_response": parsed,
            }
        ),
        "ai_brand": parsed["ai_brand"] or "",
        "ai_product_name": parsed["ai_product_name"] or "",
        "ai_product_type": parsed["ai_product_type"] or "",
        "ai_abv": parsed["ai_abv"],
        "ai_milliliters": parsed["ai_milliliters"],
        "ai_fl_oz": parsed["ai_fl_oz"],
        "ai_warning_label": bool(parsed["ai_warning_label"]),
        "ai_warning_text": parsed["ai_warning_text"] or "",
        "ai_error": parsed.get("ai_error", "") or "",
    }



## Fix the rounding of fluid measurements
def _round_hundredths(value):
    if value is None:
        return None
    try:
        return round(float(value), 2)
    except (TypeError, ValueError):
        return None


def _compute_volumes_from_raw(parsed: dict) -> dict:
    """
    Ensures both ai_milliliters and ai_fl_oz are populated.

    Rules:
    - If both exist -> do nothing
    - If only one exists -> compute the other
    - If neither exists -> attempt to use ai_volume_value + unit
    """

    ML_PER_LITER = 1000.0
    ML_PER_FL_OZ = 29.5735

    existing_ml = parsed.get("ai_milliliters")
    existing_oz = parsed.get("ai_fl_oz")

    # Try to parse existing values
    try:
        ml = float(existing_ml) if existing_ml not in (None, "") else None
    except (TypeError, ValueError):
        ml = None

    try:
        oz = float(existing_oz) if existing_oz not in (None, "") else None
    except (TypeError, ValueError):
        oz = None

    # ✅ Case 1: both exist, normalize rounding only
    if ml is not None and oz is not None:
        parsed["ai_milliliters"] = _round_hundredths(ml)
        parsed["ai_fl_oz"] = _round_hundredths(oz)
        return parsed

    # ✅ Case 2: only mL exists → compute fl oz
    if ml is not None and oz is None:
        oz = ml / ML_PER_FL_OZ
        parsed["ai_milliliters"] = _round_hundredths(ml)
        parsed["ai_fl_oz"] = _round_hundredths(oz)
        return parsed

    # ✅ Case 3: only fl oz exists → compute mL
    if oz is not None and ml is None:
        ml = oz * ML_PER_FL_OZ
        parsed["ai_milliliters"] = _round_hundredths(ml)
        parsed["ai_fl_oz"] = _round_hundredths(oz)
        return parsed

    # ✅ Case 4: neither exists → attempt fallback from raw values
    ### This requires separate data capture for raw values and units
    # raw_value = parsed.get("ai_volume_value")
    # raw_unit = (parsed.get("ai_volume_unit") or "").strip().lower()
    #
    # if raw_value in (None, ""):
    #     parsed["ai_milliliters"] = None
    #     parsed["ai_fl_oz"] = None
    #     return parsed
    #
    # try:
    #     value = float(raw_value)
    # except (TypeError, ValueError):
    #     parsed["ai_milliliters"] = None
    #     parsed["ai_fl_oz"] = None
    #     return parsed
    #
    # if raw_unit in ("ml", "milliliter", "milliliters"):
    #     ml = value
    #     oz = ml / ML_PER_FL_OZ
    # elif raw_unit in ("l", "liter", "liters"):
    #     ml = value * ML_PER_LITER
    #     oz = ml / ML_PER_FL_OZ
    # elif raw_unit in ("fl oz", "floz", "fluid ounce", "fluid ounces", "oz"):
    #     oz = value
    #     ml = value * ML_PER_FL_OZ
    # else:
    #     ml = None
    #     oz = None

    parsed["ai_milliliters"] = _round_hundredths(ml)
    parsed["ai_fl_oz"] = _round_hundredths(oz)

    return parsed
