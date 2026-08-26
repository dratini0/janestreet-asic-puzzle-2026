`default_nettype none

module adder_demo_equivalence_test (
    input  wire clk,
    input  wire rst_n,
    input  wire A,
    input  wire B,
    output wire S_original,
    output wire S_recovered_verilog,
    input  wire en
);
    adder_demo orignial (
        .clk(clk),
        .rst_n(rst_n),
        .A(A),
        .B(B),
        .S(S_original),
        .en(en)
    );

    adder_demo_recovered_verilog recovered_verilog (
        .clk(clk),
        .rst_n(rst_n),
        .A(A),
        .B(B),
        .S(S_recovered_verilog),
        .en(en)
    );
endmodule
