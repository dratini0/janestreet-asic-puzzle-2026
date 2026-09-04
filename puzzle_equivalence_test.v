`default_nettype none

module puzzle_equivalence_test (
    input  wire clk,
    input  wire rst_n,
    input  wire I,
    output wire success_recovered_verilog,
    output wire success_amaranth,
    output wire success_solution,
    output wire [7:0] O_recovered_verilog,
    output wire [7:0] O_amaranth,
    output wire [7:0] O_solution,
    input  wire enable
);
    puzzle_recovered_verilog recovered_verilog (
        .clk(clk),
        .rst_n(rst_n),
        .I(I),
        .success(success_recovered_verilog),
        .\O[0] (O_recovered_verilog[0]),
        .\O[1] (O_recovered_verilog[1]),
        .\O[2] (O_recovered_verilog[2]),
        .\O[3] (O_recovered_verilog[3]),
        .\O[4] (O_recovered_verilog[4]),
        .\O[5] (O_recovered_verilog[5]),
        .\O[6] (O_recovered_verilog[6]),
        .\O[7] (O_recovered_verilog[7]),
        .enable(enable)
    );

    puzzle_amaranth amaranth (
        .clk(clk),
        .rst(!rst_n),
        .I(I),
        .success(success_amaranth),
        .O_0_(O_amaranth[0]),
        .O_1_(O_amaranth[1]),
        .O_2_(O_amaranth[2]),
        .O_3_(O_amaranth[3]),
        .O_4_(O_amaranth[4]),
        .O_5_(O_amaranth[5]),
        .O_6_(O_amaranth[6]),
        .O_7_(O_amaranth[7]),
        .enable(enable)
    );

    puzzle_solution solution (
        .clk(clk),
        .rst(!rst_n),
        .I(I),
        .success(success_solution),
        .O(O_solution),
        .enable(enable)
    );
endmodule
