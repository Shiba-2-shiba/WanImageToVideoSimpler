import nodes
import node_helpers
import torch
import comfy.model_management
import comfy.utils

class WanImageToVideoSimper:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "positive": ("CONDITIONING", ),
                "vae": ("VAE", ),
                "width": ("INT", {"default": 1280, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                "height": ("INT", {"default": 720, "min": 16, "max": nodes.MAX_RESOLUTION, "step": 16}),
                "length": ("INT", {"default": 121, "min": 1, "max": nodes.MAX_RESOLUTION, "step": 4}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 4096}),
                "positive_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
                "clip_vision_weight": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 10.0, "step": 0.1}),
            },
            "optional": {
                "clip_vision_output": ("CLIP_VISION_OUTPUT", ),
                "start_image": ("IMAGE", ),
            }
        }

    # negativeの出力は削除し、positiveとlatentのみを返すように変更
    RETURN_TYPES = ("CONDITIONING", "LATENT")
    RETURN_NAMES = ("positive", "latent")
    FUNCTION = "encode"

    CATEGORY = "conditioning/video_models"

    def encode(self, positive, vae, width, height, length, batch_size, positive_weight, clip_vision_weight, start_image=None, clip_vision_output=None):
        latent = torch.zeros([batch_size, 16, ((length - 1) // 4) + 1, height // 8, width // 8], device=comfy.model_management.intermediate_device())
        if start_image is not None:
            # start_imageの前処理：指定のフレーム数だけ取り出し、アップスケール＆チャネル変換を実施
            start_image = comfy.utils.common_upscale(start_image[:length].movedim(-1, 1), width, height, "bilinear", "center").movedim(1, -1)
            image = torch.ones((length, height, width, start_image.shape[-1]), device=start_image.device, dtype=start_image.dtype) * 0.5
            image[:start_image.shape[0]] = start_image

            concat_latent_image = vae.encode(image[:, :, :, :3])
            mask = torch.ones((1, 1, latent.shape[2], concat_latent_image.shape[-2], concat_latent_image.shape[-1]), device=start_image.device, dtype=start_image.dtype)
            mask[:, :, :((start_image.shape[0] - 1) // 4) + 1] = 0.0

            # positiveの条件付けに対し、latent画像とマスクをウェイト付きでセット
            positive = node_helpers.conditioning_set_values(positive, {
                "concat_latent_image": concat_latent_image,
                "concat_latent_image_weight": positive_weight,
                "concat_mask": mask,
                "concat_mask_weight": positive_weight
            })

        if clip_vision_output is not None:
            # clip_vision_outputもウェイト付きでpositive条件付けに追加
            positive = node_helpers.conditioning_set_values(positive, {
                "clip_vision_output": clip_vision_output,
                "clip_vision_output_weight": clip_vision_weight
            })

        out_latent = {"samples": latent}
        return (positive, out_latent)

NODE_CLASS_MAPPINGS = {
    "WanImageToVideoSimper": WanImageToVideoSimper,
}
