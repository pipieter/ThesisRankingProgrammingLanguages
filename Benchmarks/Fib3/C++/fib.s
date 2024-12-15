	.file	"fib3.cpp"
	.text
	.p2align 4
	.globl	_Z4fib3l
	.type	_Z4fib3l, @function
_Z4fib3l:
.LFB1812:
	.cfi_startproc
	endbr64
	pushq	%r15
	.cfi_def_cfa_offset 16
	.cfi_offset 15, -16
	pushq	%r14
	.cfi_def_cfa_offset 24
	.cfi_offset 14, -24
	pushq	%r13
	.cfi_def_cfa_offset 32
	.cfi_offset 13, -32
	pushq	%r12
	.cfi_def_cfa_offset 40
	.cfi_offset 12, -40
	pushq	%rbp
	.cfi_def_cfa_offset 48
	.cfi_offset 6, -48
	pushq	%rbx
	.cfi_def_cfa_offset 56
	.cfi_offset 3, -56
	subq	$104, %rsp
	.cfi_def_cfa_offset 160
	testq	%rdi, %rdi
	je	.L117
	leaq	-1(%rdi), %rdx
	movq	%rdi, %rax
	cmpq	$1, %rdx
	jbe	.L285
	movq	$0, 80(%rsp)
	subq	$3, %rax
	movq	%rax, 72(%rsp)
	cmpq	$0, 72(%rsp)
	je	.L286
.L248:
	movq	$0, 56(%rsp)
	movq	72(%rsp), %rax
	subq	$1, %rax
	movq	%rax, 40(%rsp)
	cmpq	$0, 40(%rsp)
	movq	%rax, 88(%rsp)
	je	.L287
.L249:
	movq	$0, 24(%rsp)
	movq	40(%rsp), %rax
	subq	$1, %rax
	movq	%rax, (%rsp)
	cmpq	$0, (%rsp)
	movq	%rax, 48(%rsp)
	je	.L288
.L250:
	movq	(%rsp), %rax
	xorl	%r13d, %r13d
	subq	$1, %rax
	movq	%rax, %r12
	movq	%rax, 8(%rsp)
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	je	.L126
.L290:
	xorl	%r14d, %r14d
.L15:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %rbp
	call	_Z4fib3l
	addq	%rax, %rbp
	addq	%rbp, %r14
	cmpq	$2, %rbx
	je	.L14
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L15
	addq	$1, %r14
.L14:
	cmpq	$1, %r12
	jbe	.L116
.L291:
	movq	%r12, %rbp
	xorl	%r15d, %r15d
	.p2align 4,,10
	.p2align 3
.L17:
	movq	%rbp, %rdi
	call	_Z4fib3l
	leaq	-1(%rbp), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r15
	cmpq	$2, %rbp
	je	.L18
	subq	$3, %rbp
	cmpq	$1, %rbp
	ja	.L17
	addq	$1, %r15
.L18:
	addq	%r14, %r15
	addq	%r15, %r13
.L20:
	leaq	-3(%r12), %rax
	subq	$1, %r12
	cmpq	$1, %r12
	jbe	.L289
	movq	%rax, %r12
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	jne	.L290
.L126:
	movl	$1, %r14d
	cmpq	$1, %r12
	ja	.L291
	.p2align 4,,10
	.p2align 3
.L116:
	leaq	1(%r13,%r14), %r13
	testq	%r12, %r12
	jne	.L20
.L11:
	cmpq	$1, (%rsp)
	jbe	.L114
	movq	(%rsp), %rax
	movq	%r13, 16(%rsp)
	xorl	%r12d, %r12d
	leaq	-2(%rax), %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	je	.L128
.L293:
	xorl	%ebp, %ebp
.L24:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %r13
	call	_Z4fib3l
	addq	%rax, %r13
	addq	%r13, %rbp
	cmpq	$2, %rbx
	je	.L23
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L24
	addq	$1, %rbp
.L23:
	cmpq	$1, %r15
	jbe	.L113
.L294:
	movq	%r15, %r14
	xorl	%r13d, %r13d
	.p2align 4,,10
	.p2align 3
.L26:
	movq	%r14, %rdi
	call	_Z4fib3l
	leaq	-1(%r14), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r13
	cmpq	$2, %r14
	je	.L27
	subq	$3, %r14
	cmpq	$1, %r14
	ja	.L26
	addq	$1, %r13
.L27:
	leaq	0(%rbp,%r13), %rdx
	addq	%rdx, %r12
.L29:
	leaq	-3(%r15), %rax
	subq	$1, %r15
	cmpq	$1, %r15
	jbe	.L292
	movq	%rax, %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	jne	.L293
.L128:
	movl	$1, %ebp
	cmpq	$1, %r15
	ja	.L294
	.p2align 4,,10
	.p2align 3
.L113:
	leaq	1(%r12,%rbp), %r12
	testq	%r15, %r15
	jne	.L29
	movq	16(%rsp), %r13
	movq	%r12, %rax
.L22:
	movq	%rax, %r12
	addq	%r13, %r12
	addq	%r12, 24(%rsp)
.L30:
	movq	(%rsp), %r14
	subq	$3, %r14
	cmpq	$1, 8(%rsp)
	jbe	.L295
	movq	%r14, (%rsp)
	cmpq	$0, (%rsp)
	jne	.L250
.L288:
	movl	$1, %r13d
.L114:
	movq	24(%rsp), %rax
	leaq	1(%rax,%r13), %rax
	movq	%rax, 24(%rsp)
	movq	(%rsp), %rax
	testq	%rax, %rax
	jne	.L296
.L8:
	cmpq	$1, 40(%rsp)
	jbe	.L111
	movq	$0, 32(%rsp)
	movq	40(%rsp), %rax
	subq	$2, %rax
	movq	%rax, (%rsp)
	cmpq	$0, (%rsp)
	je	.L297
.L255:
	movq	(%rsp), %rax
	xorl	%r13d, %r13d
	subq	$1, %rax
	movq	%rax, %r12
	movq	%rax, 8(%rsp)
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	je	.L132
.L299:
	xorl	%r14d, %r14d
.L37:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %rbp
	call	_Z4fib3l
	addq	%rax, %rbp
	addq	%rbp, %r14
	cmpq	$2, %rbx
	je	.L36
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L37
	addq	$1, %r14
.L36:
	cmpq	$1, %r12
	jbe	.L110
.L300:
	movq	%r12, %rbp
	xorl	%r15d, %r15d
	.p2align 4,,10
	.p2align 3
.L39:
	movq	%rbp, %rdi
	call	_Z4fib3l
	leaq	-1(%rbp), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r15
	cmpq	$2, %rbp
	je	.L40
	subq	$3, %rbp
	cmpq	$1, %rbp
	ja	.L39
	addq	$1, %r15
.L40:
	addq	%r14, %r15
	addq	%r15, %r13
.L42:
	leaq	-3(%r12), %rax
	subq	$1, %r12
	cmpq	$1, %r12
	jbe	.L298
	movq	%rax, %r12
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	jne	.L299
.L132:
	movl	$1, %r14d
	cmpq	$1, %r12
	ja	.L300
	.p2align 4,,10
	.p2align 3
.L110:
	leaq	1(%r13,%r14), %r13
	testq	%r12, %r12
	jne	.L42
.L33:
	cmpq	$1, (%rsp)
	jbe	.L108
	movq	(%rsp), %rax
	movq	%r13, 16(%rsp)
	xorl	%r12d, %r12d
	leaq	-2(%rax), %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	je	.L134
.L302:
	xorl	%ebp, %ebp
.L46:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %r13
	call	_Z4fib3l
	addq	%rax, %r13
	addq	%r13, %rbp
	cmpq	$2, %rbx
	je	.L45
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L46
	addq	$1, %rbp
.L45:
	cmpq	$1, %r15
	jbe	.L107
.L303:
	movq	%r15, %r14
	xorl	%r13d, %r13d
	.p2align 4,,10
	.p2align 3
.L48:
	movq	%r14, %rdi
	call	_Z4fib3l
	leaq	-1(%r14), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r13
	cmpq	$2, %r14
	je	.L49
	subq	$3, %r14
	cmpq	$1, %r14
	ja	.L48
	addq	$1, %r13
.L49:
	leaq	0(%r13,%rbp), %rdx
	addq	%rdx, %r12
.L51:
	leaq	-3(%r15), %rax
	subq	$1, %r15
	cmpq	$1, %r15
	jbe	.L301
	movq	%rax, %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	jne	.L302
.L134:
	movl	$1, %ebp
	cmpq	$1, %r15
	ja	.L303
	.p2align 4,,10
	.p2align 3
.L107:
	leaq	1(%r12,%rbp), %r12
	testq	%r15, %r15
	jne	.L51
	movq	16(%rsp), %r13
	movq	%r12, %rax
.L44:
	movq	%rax, %r12
	addq	%r13, %r12
	addq	%r12, 32(%rsp)
.L52:
	movq	(%rsp), %r14
	subq	$3, %r14
	cmpq	$1, 8(%rsp)
	jbe	.L304
	movq	%r14, (%rsp)
	cmpq	$0, (%rsp)
	jne	.L255
.L297:
	movl	$1, %r13d
.L108:
	movq	32(%rsp), %rax
	leaq	1(%rax,%r13), %rax
	movq	%rax, 32(%rsp)
	movq	(%rsp), %rax
	testq	%rax, %rax
	jne	.L305
.L32:
	movq	32(%rsp), %rax
	addq	24(%rsp), %rax
	addq	%rax, 56(%rsp)
.L53:
	movq	40(%rsp), %rax
	subq	$3, %rax
	cmpq	$1, 48(%rsp)
	jbe	.L306
	movq	%rax, 40(%rsp)
	cmpq	$0, 40(%rsp)
	jne	.L249
.L287:
	movq	$1, 24(%rsp)
.L111:
	movq	56(%rsp), %rax
	movq	24(%rsp), %rsi
	leaq	1(%rax,%rsi), %rax
	movq	%rax, 56(%rsp)
	movq	40(%rsp), %rax
	testq	%rax, %rax
	jne	.L307
.L5:
	cmpq	$1, 72(%rsp)
	jbe	.L105
	movq	$0, 64(%rsp)
	movq	72(%rsp), %rax
	subq	$2, %rax
	movq	%rax, 40(%rsp)
	cmpq	$0, 40(%rsp)
	je	.L308
.L260:
	movq	$0, 24(%rsp)
	movq	40(%rsp), %rax
	subq	$1, %rax
	movq	%rax, (%rsp)
	cmpq	$0, (%rsp)
	movq	%rax, 48(%rsp)
	je	.L309
.L261:
	movq	(%rsp), %rax
	xorl	%r12d, %r12d
	subq	$1, %rax
	movq	%rax, %r15
	movq	%rax, 8(%rsp)
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	je	.L140
.L311:
	xorl	%r13d, %r13d
.L63:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %rbp
	call	_Z4fib3l
	addq	%rax, %rbp
	addq	%rbp, %r13
	cmpq	$2, %rbx
	je	.L62
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L63
	addq	$1, %r13
.L62:
	cmpq	$1, %r15
	jbe	.L104
.L312:
	movq	%r15, %rbp
	xorl	%r14d, %r14d
	.p2align 4,,10
	.p2align 3
.L65:
	movq	%rbp, %rdi
	call	_Z4fib3l
	leaq	-1(%rbp), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r14
	cmpq	$2, %rbp
	je	.L66
	subq	$3, %rbp
	cmpq	$1, %rbp
	ja	.L65
	addq	$1, %r14
.L66:
	addq	%r13, %r14
	addq	%r14, %r12
.L68:
	leaq	-3(%r15), %rax
	subq	$1, %r15
	cmpq	$1, %r15
	jbe	.L310
	movq	%rax, %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	jne	.L311
.L140:
	movl	$1, %r13d
	cmpq	$1, %r15
	ja	.L312
	.p2align 4,,10
	.p2align 3
.L104:
	leaq	1(%r12,%r13), %r12
	testq	%r15, %r15
	jne	.L68
.L59:
	movq	(%rsp), %rbp
	cmpq	$1, %rbp
	jbe	.L103
	xorl	%r15d, %r15d
	.p2align 4,,10
	.p2align 3
.L69:
	movq	%rbp, %rdi
	call	_Z4fib3l
	leaq	-1(%rbp), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r15
	cmpq	$2, %rbp
	je	.L70
	subq	$3, %rbp
	cmpq	$1, %rbp
	ja	.L69
	addq	$1, %r15
.L70:
	leaq	(%r12,%r15), %rdx
	addq	%rdx, 24(%rsp)
.L72:
	movq	(%rsp), %r13
	subq	$3, %r13
	cmpq	$1, 8(%rsp)
	jbe	.L313
	movq	%r13, (%rsp)
	cmpq	$0, (%rsp)
	jne	.L261
.L309:
	movl	$1, %r12d
.L103:
	movq	24(%rsp), %rax
	leaq	1(%rax,%r12), %rax
	movq	%rax, 24(%rsp)
	movq	(%rsp), %rax
	testq	%rax, %rax
	jne	.L314
.L56:
	cmpq	$1, 40(%rsp)
	jbe	.L101
	movq	$0, 32(%rsp)
	movq	40(%rsp), %rax
	subq	$2, %rax
	movq	%rax, (%rsp)
	cmpq	$0, (%rsp)
	je	.L315
.L265:
	movq	(%rsp), %rax
	xorl	%r13d, %r13d
	subq	$1, %rax
	movq	%rax, %r12
	movq	%rax, 8(%rsp)
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	je	.L144
.L317:
	xorl	%r14d, %r14d
.L79:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %rbp
	call	_Z4fib3l
	addq	%rax, %rbp
	addq	%rbp, %r14
	cmpq	$2, %rbx
	je	.L78
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L79
	addq	$1, %r14
.L78:
	cmpq	$1, %r12
	jbe	.L100
.L318:
	movq	%r12, %rbp
	xorl	%r15d, %r15d
	.p2align 4,,10
	.p2align 3
.L81:
	movq	%rbp, %rdi
	call	_Z4fib3l
	leaq	-1(%rbp), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r15
	cmpq	$2, %rbp
	je	.L82
	subq	$3, %rbp
	cmpq	$1, %rbp
	ja	.L81
	addq	$1, %r15
.L82:
	addq	%r14, %r15
	addq	%r15, %r13
.L84:
	leaq	-3(%r12), %rax
	subq	$1, %r12
	cmpq	$1, %r12
	jbe	.L316
	movq	%rax, %r12
	leaq	1(%r12), %rbx
	testq	%r12, %r12
	jne	.L317
.L144:
	movl	$1, %r14d
	cmpq	$1, %r12
	ja	.L318
	.p2align 4,,10
	.p2align 3
.L100:
	leaq	1(%r13,%r14), %r13
	testq	%r12, %r12
	jne	.L84
.L75:
	cmpq	$1, (%rsp)
	jbe	.L98
	movq	(%rsp), %rax
	movq	%r13, 16(%rsp)
	xorl	%r12d, %r12d
	leaq	-2(%rax), %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	je	.L146
.L320:
	xorl	%ebp, %ebp
.L88:
	movq	%rbx, %rdi
	call	_Z4fib3l
	leaq	-1(%rbx), %rdi
	movq	%rax, %r13
	call	_Z4fib3l
	addq	%rax, %r13
	addq	%r13, %rbp
	cmpq	$2, %rbx
	je	.L87
	subq	$3, %rbx
	cmpq	$1, %rbx
	ja	.L88
	addq	$1, %rbp
.L87:
	cmpq	$1, %r15
	jbe	.L97
.L321:
	movq	%r15, %r14
	xorl	%r13d, %r13d
	.p2align 4,,10
	.p2align 3
.L90:
	movq	%r14, %rdi
	call	_Z4fib3l
	leaq	-1(%r14), %rdi
	movq	%rax, %rbx
	call	_Z4fib3l
	addq	%rax, %rbx
	addq	%rbx, %r13
	cmpq	$2, %r14
	je	.L91
	subq	$3, %r14
	cmpq	$1, %r14
	ja	.L90
	addq	$1, %r13
.L91:
	leaq	0(%rbp,%r13), %rdx
	addq	%rdx, %r12
.L93:
	leaq	-3(%r15), %rax
	subq	$1, %r15
	cmpq	$1, %r15
	jbe	.L319
	movq	%rax, %r15
	leaq	1(%r15), %rbx
	testq	%r15, %r15
	jne	.L320
.L146:
	movl	$1, %ebp
	cmpq	$1, %r15
	ja	.L321
	.p2align 4,,10
	.p2align 3
.L97:
	leaq	1(%r12,%rbp), %r12
	testq	%r15, %r15
	jne	.L93
	movq	16(%rsp), %r13
	movq	%r12, %rax
.L86:
	movq	%rax, %r12
	addq	%r13, %r12
	addq	%r12, 32(%rsp)
.L94:
	movq	(%rsp), %r14
	subq	$3, %r14
	cmpq	$1, 8(%rsp)
	jbe	.L322
	movq	%r14, (%rsp)
	cmpq	$0, (%rsp)
	jne	.L265
.L315:
	movl	$1, %r13d
.L98:
	movq	32(%rsp), %rax
	leaq	1(%rax,%r13), %rax
	movq	%rax, 32(%rsp)
	movq	(%rsp), %rax
	testq	%rax, %rax
	jne	.L323
.L74:
	movq	24(%rsp), %rax
	addq	32(%rsp), %rax
	addq	%rax, 64(%rsp)
.L95:
	movq	40(%rsp), %rax
	subq	$3, %rax
	cmpq	$1, 48(%rsp)
	jbe	.L324
	movq	%rax, 40(%rsp)
	cmpq	$0, 40(%rsp)
	jne	.L260
.L308:
	movq	$1, 24(%rsp)
.L101:
	movq	64(%rsp), %rax
	movq	24(%rsp), %rcx
	leaq	1(%rax,%rcx), %rax
	movq	%rax, 64(%rsp)
	movq	40(%rsp), %rax
	testq	%rax, %rax
	jne	.L325
.L55:
	movq	64(%rsp), %rax
	addq	56(%rsp), %rax
	addq	%rax, 80(%rsp)
.L96:
	movq	72(%rsp), %rax
	subq	$3, %rax
	cmpq	$1, 88(%rsp)
	jbe	.L326
	movq	%rax, 72(%rsp)
	cmpq	$0, 72(%rsp)
	jne	.L248
.L286:
	movq	$1, 56(%rsp)
.L105:
	movq	80(%rsp), %rsi
	movq	56(%rsp), %rax
	leaq	1(%rax,%rsi), %rax
	movq	%rax, 80(%rsp)
	movq	72(%rsp), %rax
	testq	%rax, %rax
	jne	.L327
.L1:
	movq	80(%rsp), %rax
	addq	$104, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 56
	popq	%rbx
	.cfi_def_cfa_offset 48
	popq	%rbp
	.cfi_def_cfa_offset 40
	popq	%r12
	.cfi_def_cfa_offset 32
	popq	%r13
	.cfi_def_cfa_offset 24
	popq	%r14
	.cfi_def_cfa_offset 16
	popq	%r15
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L292:
	.cfi_restore_state
	addq	$1, %r12
	movq	16(%rsp), %r13
	movq	%r12, %rax
	jmp	.L22
	.p2align 4,,10
	.p2align 3
.L289:
	addq	$1, %r13
	jmp	.L11
	.p2align 4,,10
	.p2align 3
.L301:
	addq	$1, %r12
	movq	16(%rsp), %r13
	movq	%r12, %rax
	jmp	.L44
	.p2align 4,,10
	.p2align 3
.L298:
	addq	$1, %r13
	jmp	.L33
.L304:
	addq	$1, 32(%rsp)
	jmp	.L32
.L295:
	addq	$1, 24(%rsp)
	jmp	.L8
.L305:
	subq	$1, %rax
	movq	%rax, 8(%rsp)
	jmp	.L52
.L296:
	subq	$1, %rax
	movq	%rax, 8(%rsp)
	jmp	.L30
	.p2align 4,,10
	.p2align 3
.L310:
	addq	$1, %r12
	jmp	.L59
	.p2align 4,,10
	.p2align 3
.L316:
	addq	$1, %r13
	jmp	.L75
	.p2align 4,,10
	.p2align 3
.L319:
	addq	$1, %r12
	movq	16(%rsp), %r13
	movq	%r12, %rax
	jmp	.L86
.L322:
	addq	$1, 32(%rsp)
	jmp	.L74
.L313:
	addq	$1, 24(%rsp)
	jmp	.L56
.L323:
	subq	$1, %rax
	movq	%rax, 8(%rsp)
	jmp	.L94
.L314:
	subq	$1, %rax
	movq	%rax, 8(%rsp)
	jmp	.L72
.L324:
	addq	$1, 64(%rsp)
	jmp	.L55
.L306:
	addq	$1, 56(%rsp)
	jmp	.L5
.L325:
	subq	$1, %rax
	movq	%rax, 48(%rsp)
	jmp	.L95
.L307:
	subq	$1, %rax
	movq	%rax, 48(%rsp)
	jmp	.L53
.L326:
	addq	$1, 80(%rsp)
	jmp	.L1
.L327:
	subq	$1, %rax
	movq	%rax, 88(%rsp)
	jmp	.L96
.L285:
	movq	$1, 80(%rsp)
	jmp	.L1
.L117:
	movq	$0, 80(%rsp)
	jmp	.L1
	.cfi_endproc
.LFE1812:
	.size	_Z4fib3l, .-_Z4fib3l
	.section	.text.startup,"ax",@progbits
	.p2align 4
	.globl	main
	.type	main, @function
main:
.LFB1813:
	.cfi_startproc
	endbr64
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	movl	$10, %edx
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	movq	8(%rsi), %rdi
	xorl	%esi, %esi
	call	strtol@PLT
	movq	%rax, %rdi
	call	_Z4fib3l
	leaq	_ZSt4cout(%rip), %rdi
	movq	%rax, %rsi
	call	_ZNSo9_M_insertIlEERSoT_@PLT
	movq	%rax, %rbp
	movq	(%rax), %rax
	movq	-24(%rax), %rax
	movq	240(%rbp,%rax), %r12
	testq	%r12, %r12
	je	.L333
	cmpb	$0, 56(%r12)
	je	.L330
	movsbl	67(%r12), %esi
.L331:
	movq	%rbp, %rdi
	call	_ZNSo3putEc@PLT
	movq	%rax, %rdi
	call	_ZNSo5flushEv@PLT
	addq	$8, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
.L330:
	.cfi_restore_state
	movq	%r12, %rdi
	call	_ZNKSt5ctypeIcE13_M_widen_initEv@PLT
	movq	(%r12), %rax
	movl	$10, %esi
	movq	%r12, %rdi
	call	*48(%rax)
	movsbl	%al, %esi
	jmp	.L331
.L333:
	call	_ZSt16__throw_bad_castv@PLT
	.cfi_endproc
.LFE1813:
	.size	main, .-main
	.p2align 4
	.type	_GLOBAL__sub_I__Z4fib3l, @function
_GLOBAL__sub_I__Z4fib3l:
.LFB2301:
	.cfi_startproc
	endbr64
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	leaq	_ZStL8__ioinit(%rip), %rbp
	movq	%rbp, %rdi
	call	_ZNSt8ios_base4InitC1Ev@PLT
	movq	_ZNSt8ios_base4InitD1Ev@GOTPCREL(%rip), %rdi
	movq	%rbp, %rsi
	popq	%rbp
	.cfi_def_cfa_offset 8
	leaq	__dso_handle(%rip), %rdx
	jmp	__cxa_atexit@PLT
	.cfi_endproc
.LFE2301:
	.size	_GLOBAL__sub_I__Z4fib3l, .-_GLOBAL__sub_I__Z4fib3l
	.section	.init_array,"aw"
	.align 8
	.quad	_GLOBAL__sub_I__Z4fib3l
	.local	_ZStL8__ioinit
	.comm	_ZStL8__ioinit,1,1
	.hidden	__dso_handle
	.ident	"GCC: (Ubuntu 11.4.0-1ubuntu1~22.04) 11.4.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
