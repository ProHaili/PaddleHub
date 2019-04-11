import paddle
import paddle.fluid as fluid

import paddlehub as hub


def train():
    resnet_module = hub.Module(module_dir="ResNet50.hub_module")
    input_dict, output_dict, program = resnet_module.context(
        sign_name="feature_map", trainable=True)
    dataset = hub.dataset.Flowers()
    data_reader = hub.reader.ImageClassificationReader(
        image_width=224, image_height=224, dataset=dataset)
    with fluid.program_guard(program):
        label = fluid.layers.data(name="label", dtype="int64", shape=[1])
        img = input_dict[0]
        feature_map = output_dict[0]

        config = hub.RunConfig(
            use_cuda=True,
            num_epoch=10,
            batch_size=32,
            strategy=hub.finetune.strategy.DefaultFinetuneStrategy())

        feed_list = [img.name, label.name]

        task = hub.create_img_classification_task(
            feature=feature_map, label=label, num_classes=dataset.num_labels)
        hub.finetune_and_eval(
            task, feed_list=feed_list, data_reader=data_reader, config=config)


if __name__ == "__main__":
    train()