import pytest
import torch
from mmedit.models.backbones.sr_backbones.edvr import PCDAlignment, TSAFusion


def test_pcd_alignment():
    """Test PCDAlignment."""

    # gpu (since it has dcn, only supports gpu testing)
    if torch.cuda.is_available():
        pcd_alignment = PCDAlignment(mid_channels=4, deformable_groups=2)
        input_list = []
        for i in range(3, 0, -1):
            input_list.append(torch.rand(1, 4, 2**i, 2**i))

        pcd_alignment = pcd_alignment.cuda()
        input_list = [v.cuda() for v in input_list]
        output = pcd_alignment(input_list, input_list)
        assert output.shape == (1, 4, 8, 8)

        with pytest.raises(AssertionError):
            pcd_alignment(input_list[0:2], input_list)


def test_tsa_fusion():
    """Test TSAFusion."""

    # cpu
    tsa_fusion = TSAFusion(mid_channels=4, num_frames=5, center_frame_idx=2)
    input_tensor = torch.rand(1, 5, 4, 8, 8)

    output = tsa_fusion(input_tensor)
    assert output.shape == (1, 4, 8, 8)

    # gpu
    if torch.cuda.is_available():
        tsa_fusion = tsa_fusion.cuda()
        input_tensor = input_tensor.cuda()
        output = tsa_fusion(input_tensor)
        assert output.shape == (1, 4, 8, 8)
