#pragma once


struct HeuristicWeights {

    int three_blocked_stones;
    int three_half_blocked_stones;
    int three_open_stones;

    int four_blocked_stones;
    int four_half_blocked_stones;
    int four_open_stones;

    int five_open_stones;

    int capture_one;
    int capture_two;
    int capture_three;
    int capture_four;
    int capture_five;

    int stone_capture;
    int central_position;
};
