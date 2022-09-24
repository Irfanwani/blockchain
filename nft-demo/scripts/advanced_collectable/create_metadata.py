from brownie import AdvancedCollectable, network
from metadata.sample_metadata import metadata_template
from scripts.helpful_scripts import get_breed
from pathlib import Path


def main():
    advanced_collectable = AdvancedCollectable[-1]
    print(advanced_collectable)
    number_of_advanced_collectables = advanced_collectable.tokenCounter()

    print(f"You have created {number_of_advanced_collectables} Collectables")

    for token_id in range(number_of_advanced_collectables):
        breed = get_breed(advanced_collectable.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )

        collectable_metadata = metadata_template

        if Path(metadata_file_name).exists():
            print(
                f"{metadata_file_name} already exists. Please delete it to overwrite it!"
            )
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectable_metadata["name"] = breed
            collectable_metadata["description"] = f"An adorable {breed} pup!"
            print(collectable_metadata)

            image_file_name = "./img"+ breed.lower().replace("_", "-") + ".png"



def upload_to_ipfs(filepath):
    with Path(filepath).open('rb') as fp:
        image_binary = fp.read()
        ipfs_url = 'http://127.0.0.1:5001'
        enpoint = '/api/v0/add'
        