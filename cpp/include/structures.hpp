#pragma once

# include <vector>


struct  Coordinate {
    int row;
    int column;
};


struct  Alignment {
    std::vector<Coordinate> cells;
    bool                    broken;
    int                     free;
};


struct  PlayerSituation {
    std::vector<Alignment>  alignments;
    int                     captured_stones;
    int                     possible_captures;
    int                     central_position;
};