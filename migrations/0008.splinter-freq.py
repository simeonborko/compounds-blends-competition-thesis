"""Pridat stlpceky na frekvenciu vyskytu splintrov v korpuse"""

from yoyo import step


steps = [
    step(
        """ALTER TABLE splinter
        ADD sw1_splinter_freq_exact int(11) AFTER sw4_splinter_len,
        ADD sw2_splinter_freq_exact int(11) AFTER sw1_splinter_freq_exact, 
        ADD sw3_splinter_freq_exact int(11) AFTER sw2_splinter_freq_exact,
        ADD sw4_splinter_freq_exact int(11) AFTER sw3_splinter_freq_exact,
        ADD sw1_splinter_freq_any int(11) AFTER sw4_splinter_freq_exact,
        ADD sw2_splinter_freq_any int(11) AFTER sw1_splinter_freq_any,
        ADD sw3_splinter_freq_any int(11) AFTER sw2_splinter_freq_any,
        ADD sw4_splinter_freq_any int(11) AFTER sw3_splinter_freq_any
        """,
        """ALTER TABLE splinter
        DROP sw1_splinter_freq_exact,
        DROP sw2_splinter_freq_exact,
        DROP sw3_splinter_freq_exact,
        DROP sw4_splinter_freq_exact,
        DROP sw1_splinter_freq_any,
        DROP sw2_splinter_freq_any,
        DROP sw3_splinter_freq_any,
        DROP sw4_splinter_freq_any
        """,
    )
]
