<!-- Source: https://dci.dci-gitlab.cines.fr/webextranet/external_documentation_and_training_resources/index.html -->
<!-- Title: External documentation and training resources -->

<a id="external-documentation-and-training-resources"></a>

<a id="learn-resources"></a>

# External documentation and training resources

Alice, “Well, in our country, you’d generally get to somewhere else—if you ran very fast for a long time, as we’ve been doing.”
The Red Queen, “A slow sort of country! Now, here, you see, it takes all the running you can do, to keep in the same place. If you want to get somewhere else, you must run at least twice as fast as that!” Sequel to Alice’s Adventures in Wonderland, [Through the Looking-Glass](https://www.gutenberg.org/files/12/12-h/12-h.htm) by Lewis Carroll. The world is not such a race though, but what would happen if you provided less than you consume ?

In this chapter, we provide you some material to help you work efficiently with the hardware offered by Adastra.

<a id="software-engineering"></a>

## Software engineering

As the amount of scientist *man power* grows fairly linearly over time, one could say that the *complexity of coding* the physics they want to simulate increases exponentially. Indeed, they may mix and match more and more physical phenomena, and it becomes difficult to manage the complexity of the code. This section presents some resources in the hope that research teams maintaining a code base will be able to better allocate manpower.

Although one could argue that a beautiful language is one in which the programmer can easily express correct (and efficient) code, but remember that **your programming language will not save you**. Indeed, in time, everything changes, but the basics.

Programming is about writing code. The code could be good or bad and it is not a matter of personal taste. Programming is a profession. It requires constant professional education and professional ethics (A. Stepanov).

Some believe that making simple things complicated is a sign for a lack of talent or at least, may be due to a serious lack of understanding of what you are doing. In fact, one needs a sense of taste (in the aesthetic sense) when debugging, programming, and generally, for being good at something.

For HPC or realtime systems especially, we seek fast computations. To build such software, one should not primarily try to make a fast program, but to make a program that is not slow by design (prefer arrays). Then you have more optimization freedom.

Effective use of libraries and programming languages presupposes knowledge of the core areas of computer science, that is:

- Data structures and algorithms;
- Theory of computation;
- Programming languages and compilers;
- Operating systems;
- Computer architecture.

**Note**

Rapport Nivat 1983, page 10:

Le problème de la formation à l’informatique en France ne se limite malheureusement pas à l’absence de moyens: la situation réelle de la formation n’est en aucun point à la hauteur des objectifs que nous avons affichés, et plusieurs virages ont été manqués. Presque partout l’informatique n’est pas considérée comme une discipline, mais comme une fille plus ou moins légitime des mathématiques, de l’électronique ou même de la physique (suivant les endroits et les pouvoirs en place). L’enseignement officiel souffre tout à la fois de manque de temps, de manque de matériel et de manque de formateurs. Son niveau est bien en deçà des besoins : l’informatique est souvent enseignée de manière totalement utilitaire pour les besoins d’autres disciplines, sans réflexion sur sa nature (la plupart des utilisateurs demandent encore seulement des cours d’initiation à FORTRAN ou COBOL). Devant les besoins grandissants et les carences de l’enseignement officiel s’est développé un enseignement parallèle, souvent cher et de mauvaise qualité, qui délivre également un enseignement strictement utilitariste, limité à un langage de type BASIC, FORTRAN ou COBOL.

<a id="algorithm-and-generic-programming"></a>

<a id="learn-generic-programming"></a>

### Algorithm and generic programming

Before evoking the theory, remember that you run a program on a platform (OS and hardware) and that the goal of your program is just to transform data. Knowing the platform and the data transformation you have a (practical) problem. Data is and should stay the site of attention, whatever your program does. You must adapt your data (layouts) to match the problem.

Now, start with the basic, use optimal single threaded algorithm and *good* data structures, The Art of Computer Programming, Knuth, Vol. 1 [ISBN-10: 0201896834](https://isbnsearch.org/isbn/9780201896831) is a thorough start. This book (Vol. 1) or series of books (Vol. 1-4B) can serve as a reference for many algorithmic tricks.

Elements of Programming, Stepanov; McJones, [ISBN-10: 0578222140](https://isbnsearch.org/isbn/0578222140) available in [PDF](http://elementsofprogramming.com/). This book is more **practical** and focuses on writing generic code which rely on the properties of the type. Types with common subset of properties can be subject to a similar treatment. The book is a must have (and is cheap). You may also watch a few parts of the video courses dispensed at Amazon by Alexander Stepanov and available on Youtube ([part 1.1](https://www.youtube.com/watch?v=wrmXDxn_Zuc&list=PLHxtyCq_WDLV5N5zUCBCDC2WqF1VBDGg1), [part 1.2](https://www.youtube.com/watch?v=pzvG9r05fTg&list=PLHxtyCq_WDLW0NqZCcrrQUa24H_af6Mrn), [part 1.3](https://www.youtube.com/watch?v=aLgwlAtfC0w&list=PLHxtyCq_WDLXrHwcaay14-4FXdzQBIMGx), [part 2](https://www.youtube.com/watch?v=aIHAEYyoTUc&list=PLHxtyCq_WDLXryyw91lahwdtpZsmo4BGD), [part 3](https://www.youtube.com/watch?v=k-meLQaYP5Y&list=PLHxtyCq_WDLXFAEA-lYoRNQIezL_vaSX-) and [part 4](https://www.youtube.com/watch?v=c9BQnpaI58I&list=PLHxtyCq_WDLXzT_CgYPtjYab8fyd2PkjB)).

A book providing similar insights to Element of Programming but in a simpler to understand package is From Mathematics to Generic Programming, Stepanov, Alexander; Rose, Daniel, [ISBN-10: 0321942043](https://isbnsearch.org/isbn/0321942043).

The history of generic programming is presented by Sean Parent in his talk, [Generic Programming](https://www.youtube.com/watch?v=iwJpxWHuZQY).

As an aside, Dijkstra’s [note on ranges](https://www.cs.utexas.edu/users/EWD/transcriptions/EWD08xx/EWD831.html) points to some *significant* design flaws in some programming languages.

<a id="code-quality"></a>

<a id="learn-code-quality"></a>

### Code quality

Source code is the product:

- Much more time reading than writing;
- Code is the main communication channel;
- Code is documentation;
- Code is the asset;
- There is code aesthetics.

Is *complexification* the [root of the end of civilizations](https://isbnsearch.org/isbn/9780521386739) ? Keep it simple, ensure you can always apply a fix to your code and that you wont be impaired by the architecture.

**Note**

Be leery of following patterns without thoughts, this apply particularly well to this subsection.

Code quality is often set aside in the HPC world which is strange; who would trust the results of a messy, poorly understood, rarely thoroughly tested and bug or undefined behavior ridden toolkit. Writing quality lines of code is a job in itself but it may be that it is often disregarded as such, unless you face a *maintainability scalability wall*. We have seen an increasing amount of team facing porting issues or even considering rewriting their tools due to unforeseen architectural or maintainability issues.

Code quality may seem a bit abstract and in fact it is very situational, but it is real to the point where a programmer with a minimum of experience should be able to detect what is called a [code smell](https://en.wikipedia.org/wiki/Code_smell). As you write the code, you are yourself a client of this code, because you read it again, potentially you maintain it and its quality influences your ability to improve it. The quality of the code is therefore crucial and [some believe](https://youtu.be/zXCIp1ACvYI?t=3067) (from experience) that 50-60% of the time should be spent proofreading, re-factoring, correcting typos, formatting the code (maybe fixing bugs) rather than extending it with new features. This is the least you can do to avoid [software rot](https://en.wikipedia.org/wiki/Software_rot). We would like to point out that even if HPC is very much focused on computational performance, we should not forget about optimizing the readability of the software. This may need cultural, money and/or management changes. There is no such thing as *my* code and *his* code, there is *the* code. If you come across a problem, it is better to correct it directly; don’t go straight to writing a bug report, because if you leave the error now, you will lower the bar for the quality of the code, which, from experience, leads to a negative feedback loop that will degrade it further more.

You may want to test using the latest, cutting edge *stuff* but we recommend that you deploy only using the stable. Taking example with the C or C++ versions, test some of C++ 20 or C23/C++23 features but, do not rely on them and only deploy using C11/C++14 or C17/C++17. The rational is that there is too many unknown, unwritten best practices, non understood trick with the latest.

<a id="tools-and-idioms"></a>

#### Tools and idioms

Gurus and programming veterans already walked a painful path and you should follow in their steps. Do not reinvent the wheel (unless it serves as learning experience). Specify a set of rules and stick to them. Respect the common idioms of the language. A programming language is a tool, so spend time properly learning how to use it properly as you would for other tools.

One such set of rules is given [here](https://google.github.io/styleguide/cppguide.html) in the case of the C++ language. While not ideal, these rules give structure to the code and facilitate *human code parsing* (i.e. readability). Regarding the idioms, in the case of C++ two of the most famous front facing comity member, [Bjarne Stroustrup](https://www.stroustrup.com/) and [Herb Sutter](https://herbsutter.com/) offer the [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines).

There are similar [guidelines for the Fortran language](https://fortran-lang.org/en/learn/best_practices/), but they are much more scarce (a cultural issue ?).

That said, avoid projects/tools who do the largest amount of promises, shows the best website/readme, has the flashiest GIFs, appeals to the right abstract values or gets widely praised regardless of the usability of said project. There are projects which are often under the radar, because they’re not sexy and are not promising undeliverable features, but instead are just trying to do **a thing in a way that works**, and those end up almost never being mentioned, or when they are they’re mentioned as second class choices (more at loglog game <https://loglog.games/blog/leaving-rust-gamedev/#rust-gamedev-ecosystem-lives-on-hype>). Be careful of people who start with a solution and work backward to solve a problem.

One should also spend time studying tools like [Clang-format](https://clang.llvm.org/docs/ClangFormat.html), [Clang-tidy](https://clang.llvm.org/extra/clang-tidy/), the [editor config file](https://editorconfig.org/), Git and seek homogeneity across all the code base.

<a id="compiling-code"></a>

#### Compiling code

Going top bottom, the next step after defining guidelines is choosing an appropriate way to compile and expose your software for reuse. To achieve that, we use build scripts executed by build systems which are simple programs dictating amongst other things how the compiler should be called and how the compilation output (object files) should be linked. Example of tools providing such capabilities are [Make](https://en.wikipedia.org/wiki/Make_(software)) and [Ninja](https://ninja-build.org/). Some build scripts are not intended to be written by humans. While Make scripts *can* be fairly readable and maintainable, ninja’s are readable (arguably more than Make’s) but unmaintainable.

Writing such a build scripts may tie you to a build system and potentially to a platform. It also requires careful (explicit ?) dependency management, may complicate installation or packaging procedures and may require a low level understanding of the supported compiler. One advantage is that you are supposed to know exactly how it works, you coded it after all. In practice many **low level build script** are messy and poorly treated. Writing these script should be taken with as much, if not more consideration than the code itself. **Treat your build automation scripts as code, with stylistic and semantic rules.**

Some tools have been developed to abstract the build step from the system it targets. CMake was conceived to satisfy such cross-platform needs. Nowadays it is widely used by large C++ code bases. It itself does not target C++ exclusively, C and Fortran support is strong. CMake will generate many kind of build script at your leisure. It can produce scripts for Make, Ninja, VS Studio and more. CMake can ease dependency management by abstracting the use of specific compiler flag used to include headers or link against libraries, abstracting dependencies (say header visibility propagation), testing your code and [more](https://cmake.org/cmake/help/book/mastering-cmake/chapter/Why%20CMake.html).

<a id="organizing-code"></a>

#### Organizing code

Complexity is unavoidable as your code base grows but you should try to avoid convoluted designs without added value. Try to encapsulate code into namespaces, libraries and obviously, functions such that these bundle of functionalities interact through **well defined interfaces**.

Creating an interface is a delicate job that requires artful design. The best method is probably to test and try with an obviously big advantage if previous knowledge can be factored into the design. Try to keep [Hyrum’s law](https://www.hyrumslaw.com/) in mind, though its significance depend on how your users care about you not breaking the contract.

Contract, Interface, API: But what are these? An Application Programming Interface (API) can be seen as the instantiation, *in code*, of a contract. We talk of contract because indeed, there is an agreement between, in the case of computer programming, a user and a provider. What form can it take? Many, many forms, for instance what you give to `MPI_Send`, what `MPI_Send` returns, how does `MPI_Send` fails, what other effects `MPI_Send` has on the global state of the program, how you use `malloc` and `free`, how you call the `grep` command, using which protocol you exchange with your typical web server. Finally, and as Hyrum’s law reminds us, the interface is every observable behavior of, in our case, a piece of code.

Who is enforcing the contract? Sometimes, the context, the language or the library. For instance in Java, if you do an out of bound access in an array, you are promptly notified. In some cases, nobody tells you and you expose yourself to liability, say undefined or unspecified (implementation specific) behavior (see [The C and C++ languages](index.md#learn-the-c-cpp-languages)).

Generally, Keeping the interface (It) Simple (and Stupid) (KISS) is a good advice, though you should never remove necessary complexity (do not make it simpler or stupider than it need to be). Another view would be to try to use the weakest (least powerful) tool that satisfies the need or to eliminate needless diversity wherever possible (this assumes you know what you need, potentially months or years in advance). Furthermore, what kind of software would you like to work on: software so complex that the bugs aren’t obvious, or software so simple that the bugs are obvious and so there are obviously no bugs. The more technologically advanced your code is, the harder it is to correctly react when something goes wrong and the harder it’ll get to step back and try to understand the issue. Keep your code simple.

As a followup on that, some consider expertise being knowing when to stop? As opposed to knowing where to start or what to do? Indeed, the latter is easily doable using books, AI etc. but rarely are you taught when to stop adding unnecessary features. Turning something that could be simple into a feature mess is likely to be due to a lack of vision and experience, not a lack of technical knowledge.

<a id="c-the-language-of-the-birds-or-the-poor-man-s-software-glue"></a>

##### C, the language of the birds or the poor man’s software glue

“[…] the language of the birds is postulated as a mystical, perfect divine language, Adamic language, Enochian, angelic language or a mythical or magical language used by birds to communicate with the initiated”, [Language of the birds, Wikipedia](https://en.wikipedia.org/wiki/Language_of_the_birds).

Interfaces take many forms, though in our case we shall focus on **the use of C to provide stable interfaces between languages**. The C language is the *glue* of computer science because it’s ubiquitous, low-level, stable (in time) and simple. (That said, maybe the *glue* is getting old.) By stable, we mean the [Application Binary Interface (ABI)](https://en.wikipedia.org/wiki/Application_binary_interface) is stable. For instance, the way you pass arguments in registers or on the stack before calling, they way you name your symbols (the string that marks, say, your global variables and your functions in object files), that, almost never changes for a given platform.

As an example, say you recompiled your code using a different Fortran or C++ standard (C++03, C++17 etc.) but you kept the same compiler or that you changed compiler, know that the [interface could change](https://en.wikipedia.org/wiki/Name_mangling#How_different_compilers_mangle_the_same_functions) (and in certain cases, **will** change). The ABI changed to be precise, and indeed, the representation of the symbols may have changed and thus, so does the interface of your library, even though the service your libraries provides probably hasn’t changed. In the C language, symbols are very likely **not** to change for a given platform.

What was subject to changes between compiler or language version in the example above is the symbol naming scheme which is called mangling. This is a *workaround* to linkers not being aware of the languages specific features. Say C’s calling convention, C++’s namespaces or overloading and Fortran’s modules. The language specificities get mangled into a string which will become the symbol. This used to be one of reason as to why building C++ from source using an unique compiler was often a relief, you get strong guarantees, that you will not mix multiple mangling schemes.

For obvious reasons, the C mangling is very much tied to the platform, else you can not talk with the OS anymore. So the issue comes from the fact that on a similar platform, compilers can emit different symbols from a similar code (though that tends to change, as everything gets LLVM based nowadays, and people want to use shared libraries). As a side note, the C language is popular with most large OS.

Anyway, because everybody talk C, it is a good candidate to talk with other programming languages. You will find C *bindings* for Python, Go, Fortran ISO C (`bind(c)`), Java, etc.. These bindings are just wrappers in language C around a code in language *L0*, themselves often used in language *L1*. If you think about it, it may remind you of a funnel or of an hourglass (see [Other resources](index.md#learn-organizing-code-resources)).

**Note**

Inside a program using a *fixed* language (say only C++), ABI concerns can be reduced as sources are often compiled using a single compiler and as such, the code is conceived by the compiler so it can talk to itself.

**Warning**

Assuming the following C functions declarations `void func_a();` and `void func_a(int);`. Note that both map to the **same** `func_a` symbol.

Finally, there are some symbol **visibility issues** that you may encounter with shared libraries. We do not go down this rabbit hole but provide additional documents [here](index.md#learn-organizing-code-resources). (TLDR; use the following flags `-shared -fPIC -fvisibility=hidden -Bsymbolic` when building shared libraries).

<a id="fortran-an-historical-chaos-of-practicality"></a>

##### Fortran, an historical chaos of practicality

When building an *interoperability* layer in the Fortran language, you have at least two solution, use C symbol names and Fortran function interface using `BIND(C, NAME='<my C symbol name>')` and the `ISO_C_Binding` module. Or, assume that the caller will know how to call Fortran functions or that the C code will mimic the Fortran implementation’s ABI.

The second option is unfortunately horribly annoying to use. At least, one must know and check the following assuming a routine called `Add`/`ADD`/`ADd` etc.:

- the name and space alterations necessary to make a C routine callable from Fortran77. The options are:
  :   - `add_`: All F77-callable C routines should be lowercase, and have an underscore suffixed to their names;
      - `add__`: All F77-callable C routines should be lowercase, have an underscore suffixed to their names, and if the F77 name itself possesses an underscore, two underscores should be suffixed;
      - No change: All F77-callable C routines should be lowercase, with no name alteration;
      - Upper case: All F77-callable C routines should be made uppercase, with no further name alteration.
- the mapping between F77’s INTEGER and the appropriate C integral type. Options are:
  :   - F77’s INTEGER is C’s integer: F77’s INTEGER corresponds to C’s integer;
      - F77’s INTEGER is C’s long: F77’s INTEGER corresponds to C’s long;
      - F77’s INTEGER is C’s short: F77’s INTEGER corresponds to C’s short.
- F77 string handling. The options are:
  :   - String Sun style: The string’s address is passed at the string’s location on the stack, and the string’s length is then passed as an F77_INTEGER after all explicit stack arguments;
      - String Cray style: Special option for CRAY machines, which uses Cray’s fcd (fortran character descriptor) for interoperation;
      - String struct pointer: The address of a structure is passed by a Fortran77 string, and the structure is of the form `struct {char *cp; F77_INTEGER len;};`;
      - String struct value: A structure is passed by value for each Fortran77 string, and the structure is of the form `struct {char *cp; F77_INTEGER len;};`.

Now, good luck checking all that.

<a id="example"></a>

##### Example

You have a Fortran code named *LA* using a C++ library *LB* itself using an other C++ library *LC*. What can you do? First, between Fortran and C++, you will have to rely on things like the Fortran 2003’s [ISO C binding constants](https://fortranwiki.org/fortran/show/iso_c_binding) and a C99 interface. For the C++ code, either you can guarantee that both *LB* and *LC* get compiled by the same compiler or at least, that different compilers use a similar symbol naming scheme. Or, you wrap the services provided by library *LC* in a C99 interface.

<a id="semantic-versioning"></a>

#### Semantic versioning

When your code reaches a state at which it contains enough changes that it would be worthwhile for the users to upgrade or at least to publish, one can do a version bump. The idea with [semantic versioning](https://semver.org/) is to provide through the version, information about how the interface evolves:

1. MAJOR version when you make incompatible API changes;
2. MINOR version when you add functionality in a backwards compatible manner;
3. PATCH version when you make backwards compatible bug fixes.

You then concatenate `MAJOR.MINOR.PATCH` to form a version tag which you could use to mark your Git commits and release tarballs.

Reading the [semver.org](https://semver.org/) FAQ should provide you with the appropriate insights regarding software interface management and complexities justifying the role of a *norm* for version labeling.

<a id="other-resources"></a>

<a id="learn-organizing-code-resources"></a>

#### Other resources

Some CMake guidelines are given by Manuel Binna in [Effective Modern CMake](https://gist.github.com/mbinna/c61dbb39bca0e4fb7d1f73b0d66a4fd1).

Stefanus DuToit presents some aspects of the Hourglass concept in [Hourglass Interfaces for C++ APIs](https://youtu.be/PVYdHDm0q6Y?t=106).

Organize your code in library, this is common, but often wrongly done. Some details are given by Ulrich Drepper in [`How To Write Shared Libraries`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/0592827c5341978198a1893b54d93e4b/dsohowto.pdf).

[GCC’s documentation on symbol visibility](https://gcc.gnu.org/wiki/Visibility) is an important read when dealing with libraries. Know that [CMake provides tools to produce symbol visibility helper macros](https://cmake.org/cmake/help/latest/module/GenerateExportHeader.html).

Some of Linux’s dynamic libraries implementation issues are discussed in [Sorry state of dynamic libraries on Linux](https://web.archive.org/web/20170722161806/https://macieira.org/blog/2012/01/sorry-state-of-dynamic-libraries-on-linux) by Thiago Macieira and [Everything You Ever Wanted to Know about DLLs](https://www.youtube.com/watch?v=JPQWQfDhICA) by James McNellis. A recent talk given at CppCon by Ofek Shilon gives insights on [Linkers, Loaders and Shared Libraries](https://youtu.be/_enXuIxuNV4?t=24).

Some interesting design edition to simplify C++ API and readability are given by Björn Fahller in [Typical C++, But Why?](https://www.youtube.com/watch?v=ZJKWNBcPHaQ)

Some notes on undefined behavior are given by Fedor Pikus in [this talk](https://www.youtube.com/watch?v=k9N8OrhrSZw).

One should be aware of the out-of-bound access issues introduced by buggy algorithms. While tools exist to try to circumvent these issues, it is possible to use C++ to, in a lightweight way, provide performance and increased safety under the form of *illegal operation = crash*. Thus limiting silent corruption which to be fair, may be one of the most horrendous nightmare to debug. Tristan Brindle [presents a library](https://www.youtube.com/watch?v=nDyjCMnTu7o) (unfortunately limited to C++20 and up) that implements his ideas on using indices instead of iterators as a way to force dereference in full context regarding the state and size of a container. This is clearly not something you want in tight kernels, though we could see many use cases for more common code, dealing notably with initialization, communications, restart and general data block management across operators, host and device.

A portable code is an illusion. You can reduce the hurdle of porting a code to an architecture (hardware) by smartly/tastefully designing the architecture or the code but you can’t make a given piece of code portable everywhere (while also using the hardware efficiently). For an architecture, there are ported code and not ported code. A portable code is an illusion, and the span of this illusion should be yours to decide. Do you want to support Android or, are CUDA, HIP and Sycl devices enough ? More on the subject in [this document](../porting_optimization/index.md#porting-optimization-porting-to-gpu).

Reducing the amount of dependency limits the hurdles of porting a code and in the recent years we have observed a significant trend towards having a lot of low level code (C/C++) dependencies. This is a fundamentally dangerous idea because older low level code is not as versatile in its package management as higher level language like Python or JavaScript. Then researchers have to rely on tools such as EasyBuild or Spack because its impossible to build their own tools by hand. We understand that what is being said right now goes against the typical *modern* wisdom of having libraries for everything. A middle ground needs to emerge but the current *carry on regardless* stance towards adding a bunch of libraries and **unnecessary abstraction**, we consider it harmful.

<a id="the-c-and-c-languages"></a>

<a id="learn-the-c-cpp-languages"></a>

### The C and C++ languages

If one seeks insights into the original intended use of the C++ standard library, Bob Steagall presents [Back to Basics: Classic STL](https://www.youtube.com/watch?v=tXUXl_RzkAk). Obviously, as Alexander Stepanov heavily contributed to what was called the Software Technology Lab (STL) or Standard Template Library (STL) or Stepanov And Lee (STL) library, one should also take a look at the documents he produced. Some of which are and presented in the [Algorithm and generic programming](index.md#learn-generic-programming) subsection.

Undefined Behavior (UB) is a plague unfortunately found if many if not all codes. In C, C++ and Fortran it is particularly pervasive. Sometimes, UB is used to promote an optimization, but it is unfortunately often involuntary. A nice read is given by Chris Lattner on the LLVM blog: [What Every C Programmer Should Know About Undefined Behavior](https://blog.llvm.org/2011/05/what-every-c-programmer-should-know.html). See [Sanitizers](../software_stack/tools/index.md#adastra-software-stack-tools-debugging-sanitizer) for tools to protect against some cases of UB. Some example of UB are given in [P1494R4: Partial program correctness](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2024/p1494r4.html).

David R. Tribble gives a list of discrepancies between C and C++ in Incompatibilities Between ISO C and ISO C++ <http://david.tribble.com/text/cdiffs.htm#C99-static-linkage>. This discrepancies are important to understand if one whishes to write correct, easy to port code.

In 2024, David Sankel gave the [C++ Should Be C++](https://www.youtube.com/watch?v=qTw0q3WfdNs) talk. It describes some issues related to the C++ standard committee somewhat blindly adding features to the standard. This talk is originated from this C++ proposition [C++ Should Be C++ P3023R1, 2023-10-31](https://www.open-std.org/JTC1/SC22/WG21/docs/papers/2023/p3023r1.html). Some people are aware of the issue and raising the bell, and some for have been doing so for a long time: [Nicolai Josuttis in 2024](https://www.youtube.com/watch?v=c1gfbbE2zts), Stroustrup in 2015, [Thriving in a Crowded and Changing World: C++ 2006-2020 page 70/110](https://dl.acm.org/doi/pdf/10.1145/3386320) and [Thoughts about C++17](https://open-std.org/jtc1/sc22/wg21/docs/papers/2015/n4492.pdf), [Direction For ISO C++, page 30: The C++ Programmers’ Bill of Rights](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2022/p2000r4.pdf), [How can you be so certain?](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2019/p1962r0.pdf), [What’s all the C Plus Fuss? Bjarne Stroustrup warns of dangerous future plans for his C++](https://www.theregister.com/2018/06/18/bjarne_stroustrup_c_plus_plus/), [this meeting](https://youtu.be/Bycec3UQxOc?t=2478) and more recently, worries about [C++26 becoming too unfocused](https://www.youtube.com/watch?t=1229&v=R2ulYtpV_rs). Still some continue to propose underdeveloped or poorly designed features for inclusion into the standard. Some committee members seem to focus on pursuing personal ambitions instead of addressing the needs of the whole language community. Since C++20, concerns have been growing about the often rarely useful features or useful for expert but not to the majority of the programmers. Though, some say simplicity is an [emergent property of a language](https://www.youtube.com/watch?v=PFdWqa68LmA), except, if interfaces are leaky, one then needs to understand all the shenanigans going on under to start making sense of the whole.

<a id="floating-point-computation"></a>

### Floating point computation

<a id="ieee-754-floating-point"></a>

#### IEEE 754 Floating point

The representation (or the approximation) of the real numbers comes in many flavors. One of which is the floating point [`IEEE754 standard`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/92fab3c40657de2d34127e8ffd1f1d31/IEEE754_2008.pdf). Representing reals in such a way requires obvious concessions and has non obvious side effects. David Goldberg’s [What Every Computer Scientist Should Know About Floating-Point Arithmetic](https://docs.oracle.com/cd/E19957-01/806-3568/ncg_goldberg.html) is a recommended introduction.

A note on the concept of Unit in the Last Place (ULP) is given by Jean-Michel Muller in [`On the definition of ulp(x)`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/3dcece7eb6f5e034991e8d171c994c5b/muller.ulp.pdf).

When porting code from CPU to GPU, one should not expect bit perfect results on bot architecture. Expecting bit perfect result reproduction is an illusion as one can not control parallel reduction order (except at some cost), nor can he control the usage of Fused Multiply Add (FMA), unrolling, floating point operation reordering, hardware implemented transcended function etc. (except, again, at the cost of performance). Anyway, one should expect discrepancies some of which are described in [`Precision & Performance: Floating Point and IEEE 754 Compliance for NVIDIA GPUs`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/fe9d8d8e3d36dff1d36831c76641a2b6/whitehead.gpu_accuracy_precision.pdf) by Nathan Whitehead and Alex Fit-Florea.

<a id="numerical-computation-oriented-algorithm"></a>

#### Numerical computation oriented algorithm

While by **far** not a book on coding best practices (too bad they don’t lead by example), Numerical Recipes 3rd Edition: The Art of Scientific Computing, [ISBN-10: 0521884071](https://isbnsearch.org/isbn/9780521884075) can present the basics of many computations technics, tricks and concepts.

In addition to what Knuth proposes, you can take a look at the numerical algorithm shown in Introduction to Algorithms, 3rd Edition, [ISBN-10: 0262033844](https://isbnsearch.org/isbn/9780262033848).

<a id="numerical-analysis"></a>

#### Numerical analysis

Accuracy and Stability of Numerical Algorithms 2nd Edition, Higham, Society for Industrial and Applied Mathematics, [ISBN-10: 0898715210](https://isbnsearch.org/isbn/9780898715217).

**Note**

Precision refers to the *sample spacing*. Accuracy relate how close to *reality* a value is, as such, it connect a value to the context in which it is used.

<a id="concurrency-for-parallel-software"></a>

<a id="learn-concurrency"></a>

### Concurrency for parallel software

Concurrency is the ability of an algorithm to produce the expected result when part of it are executed with relaxed ordering, that is, not necessarily sequentially. As an example \(a \times b + c \times d\) contains two multiplications which could be executed in any order: left then right or right then left. The two resulting intermediate value would not change. Without concurrency you will not scale on HPC clusters as this concurrency is what allows for parallelism, that is, distribution of the work on multiple processing units.

So, your concurrent operations end up being scheduled onto the hardware by a scheduler (which could be the hardware itself or an operating system). A scheduler is responsible for dispatching the threads of execution on hardware resources and providing guarantees when a given thread’s operations may be considered for execution. Different *levels* of guarantee exist and are provided by different schedulers:

- the *maximal* guarantee scheduler specifying that *all threads eventually execute their next step*;
- the *minimal* guarantee scheduler specifying that *at least one thread executes its next step*.

In the C++ memory/concurrency model (which is pervasive to the whole industry), the concept of **step** is defined as:
- when a thread of execution performs an operation that synchronizes: mutex operations, accessing a `volatile` or atomic;
- when a thread of execution starts (fork) or ends.

The *steps* of a thread of execution are ordered using the sequenced before/after relation.

**Note**

A blocking operation can be defined as an operation attempting to make an undetermined amount of internal *step*.

Some guarantees can be given to a program:
- concurrent forward-progress: under the *maximal* guarantee scheduler;
- parallel forward-progress: *threads that have executed a step eventually execute their next step* and *at least one thread that is blocked-on eventually executes its first step*;
- weak(ly) parallel forward-progress: *at least one thread that is blocked-on eventually executes its next step*.

From this, multiple issues can occur such as:
- a wait;
- a lock;
- an obstruction;
- a clash;
- a starvation/livelock which occurs when a program exceeds the scheduler’s guarantees;
- a deadlock which occurs when a program exceeds the **maximal guarantee scheduler**’s guarantees.

Concurrent forward-progress is what the typical operating systems such as Linux or Windows should offer (modulo extreme thread priorities).

On SIMD, we get weak parallel forward-progress. This mean you should never say, take a lock in a SIMD operation, indeed if at least 2 lanes of a SIMD operation try to take the same lock, we get a livelock, we exceeded the scheduler’s guarantees.

On Nvidia GPUs, since the Volta microarchitecture, we have what is called independent thread scheduling. It can be understood as SIMD/SIMT but with an individual program counter for each SIMD lanes, allowing the scheduler to *give the progress of blocking lanes* to make progress on other threads when a `__syncwarp` (or AFAIK other synchronization semantic) call is made. It also seems to allow switching from stalled lanes to another set of converged lanes. This allows a wider class of algorithm to run on GPU but is not there for performance reason. This independent thread scheduling makes Volta an later Nvidia architectures provide parallel forward-progress. AMD GPUs are pure SIMD machines, they provide weak parallel forward-progress. Since Volta, on Nvidia GPUs, SIMD has become an optimization (which in practice is the most used runtime mode).

On the nature of progress by Herlihy M. and Shavit N and [Forward Progress Guarantees in C++](https://www.youtube.com/watch?v=g9Rgu6YEuqY) by Olivier Giroux expose the concepts above. Additional notions are given by Bryce Adelstein Lelbach in [The C++ Execution Model](https://youtu.be/1-OcraaQl8M?t=1003).

In [`Is Parallel Programming Hard, And, If So, What Can You Do`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/f99bd1bc95bf41ab711aa898ce0b4060/perfbook.2011.01.02a.pdf), Paul E. McKenney helps *you understand how to program shared-memory parallel machines without risking your sanity*.

The notion of implicit vs explicit SIMD is significant for people wanting to abstract devices under a software layer. It was discussed as far back as the inaugural OpenCL session at HotShip 21 (2009) <https://www.youtube.com/watch?t=2341&v=RnAsDGmWp3I>. Basically, it refers to either user/compiler (explicit) driven vectorization like usually done on CPU, vs hardware (implicit) driven vectorization (GPU). For GPU, you program a single SIMD lane with a program taking a index (potentially multi dimensional, `threadIdx`, `blockIdx` etc.) as input which is used to represent an amount of work referred to as a work item. The instantiation of this program on lanes is referred to as SPMD (like MPI).

Instruction Level Parallelism (ILP) plays a major role in CPU kernel optimization, notably due to the out of order issuing of instruction. Tools like <https://uica.uops.info/> provide significant insights.

<a id="atomic-operations"></a>

#### Atomic operations

Atomic operation are *tricky* to say the least. Herb Sutter’s [atomic Weapons part 1](https://www.youtube.com/watch?v=A8eCGOqgvH4), [atomic Weapons part 2](https://www.youtube.com/watch?v=KeLBd2EJLOU), Frank Birbacher’s [Atomic’s memory orders, what for?](https://www.youtube.com/watch?v=A_vAG6LIHwQ) and Fedor Pikus’s [Concurrency in C++: A Programmer’s Overview part 2](https://www.youtube.com/watch?v=R0V4xJ9HZpA) present some of the complexity. Two other recommended documents are the [GCC documentation section](https://gcc.gnu.org/wiki/Atomic/GCCMM/AtomicSync) and the [cppreference section](https://en.cppreference.com/w/cpp/atomic/memory_order) on atomic memory orders.

Although Fedor Pikus’s [Concurrency in C++: A Programmer’s Overview part 1](https://www.youtube.com/watch?v=ywJ4cq67-uc) and [Concurrency in C++: A Programmer’s Overview part 2](https://www.youtube.com/watch?v=R0V4xJ9HZpA) are directed toward a C++ audience, the concepts involved are **key** to good parallel software design. In part 2, it notably presents **atomic** operations and some of their pitfalls.

<a id="parallel-programming-using-openmp"></a>

#### Parallel programming using OpenMP

<a id="official-documentation"></a>

##### Official documentation

[`OpenMP specification v4.5`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/e7240ba79df7fe7843251c2a8379e741/OpenMP-API-Specification-4-5.pdf) and [`OpenMP specification v5.1`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/b50cdea99af31163fb5deb2bebafbde1/OpenMP-API-Specification-5-1.pdf). Maybe more importantly, the [`OpenMP specification v5.0 Examples`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/1ed61e5baf6c542d3b1672efce282939/openmp-examples-5-0-1.pdf) or, as [a website](https://passlab.github.io/Examples/contents/Title_Page.html).

[LLVM shares a web pages](https://clang.llvm.org/docs/OpenMPSupport.html#openmp-5-0-implementation-details) tracking the implementation state of standard OpenMP features.

<a id="courses"></a>

##### Courses

The best publicly available courses are probably the ones given by some of the OpenMP standardization committee members themselves. EUROfusion dispensed such courses which are now available on Youtube ([Part 1: Introduction](https://www.youtube.com/watch?v=WKMuhZvBATY), [part 2: Tasking](https://www.youtube.com/watch?v=Ywjc5foDoZQ), [part 3: NUMA and SIMD](https://www.youtube.com/watch?v=U1s0NOJirLE), [part 4: Offloading](https://www.youtube.com/watch?v=y6mpVhx0EEE) and [part 5: Advanced offloading](https://www.youtube.com/watch?v=K-znotPWrPc)). The courses’ resources are available [here](https://indico.euro-fusion.org/event/688/).

When dealing with GPUs though, most of the CPU knowledge does not old anymore. New assumption must be used to properly map OpenMP concepts to the GPU. These are well documented in [Utilizing LLVM/OpenMP to the Fullest by Johannes Doerfert](https://www.youtube.com/watch?v=R9PUdx1ya1o). It is **highly** recommended that any OpenMP target user understand this content.

<a id="compiler-infrastructure"></a>

<a id="learn-openmp-implementation-compiler"></a>

### Compiler infrastructure

Compilers are complex machinery. We can try providing some insights on the service in renders us, mostly in the form of optimizations.

<a id="openmp-optimization"></a>

#### OpenMP optimization

LLVM provides a C and C++ compiler called Clang. It ships with an OpenMP implementation and some work is being put into adding optimization passes that are OpenMP aware. This has gained more traction with the inclusion of accelerator as target for OpenMP.

Johannes Doerfert provides some (old but valid) insights on the internals of OpenMP in LLVM in [Compiler Optimizations for OpenMP Accelerator Offloading](https://www.youtube.com/watch?v=3AbS82C3X30). The talk is available in a [longer and more thorough version](https://www.youtube.com/watch?v=eIMpgez61r4). A more recent talk by Eric Wright informs us of the role `omp simd` could play in LLVM’s OpenMP target GPU support: [GPU Warp-Level Parallelism in LLVM/OpenMP](https://www.youtube.com/watch?v=7RfJQNqn_H8). If you wish to dig more into subject, we recommend the following papers and presentations:

- [`Bertolli, Carlo, et al. "Coordinating GPU threads for OpenMP 4.0 in LLVM." 2014 LLVM Compiler Infrastructure in HPC. IEEE, 2014`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/6623e2409aaefa352fd4c7ff7d719b3f/bertolli.2014.pdf);
- [`Samuel Antao "LLVM Support for OpenMP 4.0 Target Regions on GPUs." Supercomputing 2014`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/347bc0ba8b014acb0e780399fabdb79b/antao.2014.pdf);
- [`Jacob, Arpith Chacko, et al. "Efficient fork-join on GPUs through warp specialization." 2017 IEEE 24th International Conference on High Performance Computing (HiPC). IEEE, 2017`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/5554175e6f83a9aa97f21457014d6b99/jacob.2017.pdf);
- [`Tiotto, Ettore, et al. "OpenMP 4.5 compiler optimization for GPU offloading." IBM Journal of Research and Development 64.3/4 (2019): 14-1`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/14eff130b1f21fef61eca8ed2f88ee18/tiotto.2019.pdf) and
- [`Huber, Joseph, et al. "Efficient execution of OpenMP on GPUs." 2022 IEEE/ACM International Symposium on Code Generation and Optimization (CGO). IEEE, 2022`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/7307eee065007ff850ec39e5db473914/huber.2022.pdf).

Some of the LLVM OpenMP backend developer present ideas on [OpenMP Parallelism-Aware Optimizations](https://www.youtube.com/watch?v=gtxWkeLCxmU).

Also, [GCC OpenMP implementation documentation](https://gcc.gnu.org/onlinedocs/libgomp) and the source code of the [GCC](https://github.com/gcc-mirror/gcc/tree/master/libgomp) or the [LLVM](https://github.com/llvm/llvm-project/tree/main/openmp) implementation can be of interest.

<a id="generating-pseudo-random-numbers"></a>

### Generating (pseudo) random numbers

Generating random numbers is often misunderstood, based on faulty design and thus, often misused. That is, most codes **are just wrong**. [Walter E. Brown gives some insight](https://www.youtube.com/watch?v=6DPkyvkMkk8) on the history of Pseudo Random Number Generator (PRNG) in the C and C++ languages, and then gives some notes on code patterns to avoid.

<a id="cpu-programming"></a>

### CPU programming

A classical introduction read on CPU micro architecture is given by Jason Robert Carey Patterson in [Modern Microprocessors A 90-Minute Guide!](https://www.lighterra.com/papers/modernmicroprocessors/).

Memory is core to the Von Neumann computer architecture. Most HPC software are memory bound, that is, their performance is primarily dictated by the speed at which the data in main memory (RAM) can be accessed. One should know some basics on how it behaves, what are the software pitfalls. Ulrich Drepper presents RAM and memory controller hardware design and maybe most importantly to the reader, CPU caches details in [What every programmer should know about memory](https://lwn.net/Articles/250967/).

<a id="understanding-the-zen-4-genoa-cpu"></a>

<a id="learn-zen4-genoa"></a>

#### Understanding the Zen 4 Genoa CPU

User *clamchowder* on chipsandcheese.com gives some insights on the inner working of the Zen4 architecture. In [part 1](https://chipsandcheese.com/2022/11/05/amds-zen-4-part-1-frontend-and-execution-engine/), the predictors, register renaming, out of order execution and AVX512 capabilities of the microarchitecture are evoked. In [part 2](https://chipsandcheese.com/2022/11/08/amds-zen-4-part-2-memory-subsystem-and-conclusion/), the cache hierarchy, core to core latency, store and load latency and memory throughput are mentioned.

<a id="gpu-programming"></a>

### GPU programming

<a id="basics"></a>

#### Basics

In addition to what [we present in the porting guide](../porting_optimization/index.md#porting-optimization-performance-tuning-monitoring-gpu-specific-guidelines) we proposes a lot of external document.

[CppCon 2016: “Bringing Clang and C++ to GPUs: An Open-Source, CUDA-Compatible GPU C++ Compiler”](https://www.youtube.com/watch?v=KHa-OSrZPGo), [PRACE Multi GPU courses](https://github.com/FZJ-JSC/tutorial-multi-gpu/), [PRACE HIP courses](https://github.com/csc-training/hip), [GPU Hackathon](https://www.openhackathons.org/s/technical-resources), [GPU Computing: Past, Present & Future](https://www.youtube.com/watch?v=3OX_tqGGgfQ) by Ian Buck.

A more complete set of example, exercise and slides is provided through this AMD course:

- [`01. Introduction to AMD Architecture and APU_Programming_Model`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/8ad11d4e2b1d82201528796cf3b6fc28/01.%20Introduction%20to%20AMD%20Architecture%20and%20APU_Programming_Model.pdf)
- [`02. Introduction to HIP_and_ROCm`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/c818fc50e73707ff2cb786e10cb1d962/02.%20Introduction%20to%20HIP_and_ROCm.pdf)
- [`03. Introduction_to_OpenMP_Offload`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/3522c1ec7b5b5b73f17b14eeb4721ecc/03.%20Introduction_to_OpenMP_Offload.pdf)
- [`04. Introduction_to_profiling`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/1fef1603046412eecd199f689973ef19/04.%20Introduction_to_profiling.pdf)
- [`05. Advanced HIP`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/f3d177e4afc5d23f17af2cfdcf173491/05.%20Advanced%20HIP.pdf)
- [`06. Advanced OpenMP and Language Constructs`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/642cf583df48f40951f6feae33373784/06.%20Advanced%20OpenMP%20and%20Language%20Constructs.pdf)
- [`07. OpenMP_and_HIP_Interoperability`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/3de031a3d70f758d4598dab2791b3373/07.%20OpenMP_and_HIP_Interoperability.pdf)
- [`08. Performance Portability frameworks (Kokkos, Raja, C++Std Parallelism, etc)`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/cb87ff28e893d93e72b1fc4ffeb241a0/08.%20Performance%20Portability%20frameworks%20%28Kokkos%2C%20Raja%2C%20C%2B%2BStd%20Parallelism%2C%20etc%29.pdf)
- [`09. GPU-Aware_MPI and Ghost Exchange`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/8ec8b9d52c5c5a2b3e76a49ecd7f6b5b/09.%20GPU-Aware_MPI%20and%20Ghost%20Exchange.pdf)

<a id="advanced"></a>

#### Advanced

If at the kernel level, GPU and CPU code could have similarities, the biggest difference is in the way to address the memory hierarchy. By this, understand having to copy from host to device but even more importantly, that cache blocking as done heavily on CPU, through implied caching and large L1D/L2D wont work on GPUs. GPU offer very little cache space normalized to the SIMD lane count.

A good introduction is given by dissecting the anatomy of an optimized GEMM on GPU implementation by Scott Gray in [A full walk through of the SGEMM implementation](https://github.com/NervanaSystems/maxas/wiki/SGEMM).

<a id="understanding-the-amd-mi250x-gpu"></a>

<a id="learn-mi250x"></a>

#### Understanding the AMD MI250X GPU

In 2014, Layla Mah presented [`the GCN architecture`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/7ce42fb9fb3b40a6ebe4b5ba7d25b657/GCN_Architecture.pdf) of which the CDNA architecture inherits many specificities.

AMD offers in depth details on [the Compute Unit (CU)](https://rocm.docs.amd.com/projects/omniperf/en/latest/conceptual/compute-unit.html), [the VALU, SALU, LDS](https://rocm.docs.amd.com/projects/omniperf/en/latest/conceptual/pipeline-descriptions.html#pipeline-descriptions), [some generic terminology](https://rocm.docs.amd.com/projects/omniperf/en/latest/conceptual/definitions.html)

AMD presented [`some generalities on the Cray blades that Adastra has`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/b3150a2d0d48ffa3edc3e608cfd9a410/cray.amd.MI200.node.architecture.pdf).

Some notes on [AMD’s Instinct MI200 Architecture](https://chipsandcheese.com/2022/09/18/hot-chips-34-amds-instinct-mi200-architecture/) and [AMD Instinct MI200 Series Accelerator and Note Architectures](https://youtu.be/hxcAA32Htt0?t=2604).

Carl Pearson of Sandia National Laboratories (SNL) exposed some ways to exchange data between CPU and MI250X and presented it in [`Interconnect Bandwidth Heterogeneity on AMD MI250x and Infinity Fabric`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/93014207409a3d925f024606f99c0d3f/cpearson_mi250x_copy.pdf).

Folks at Juelich Computing Center (JSC) did some benchmarking on the communication speeds between GCDs in [First Benchmarks with AMD Instinct MI250 GPUs at JSC](https://x-dev.pages.jsc.fz-juelich.de/2022/08/01/mi250-first-performances.html).

The AMD GPGPU software stack is called ROCm and rely on the ROCt and ROCk software. ROCt serves as the interface for talking to the kernel’s AMD GPU driver ROCk. The ROCt interface implements the [Heterogeneous System Architecture (HSA)](https://hsafoundation.com/) [`interface`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/8dc8354f3d5b601d7d668192ba92ffc3/HSA-SysArch-1.2.pdf). So the AMD HIP runtime talks to the OS kernel through an HSA interface and the kernel talks to the GPU.

AMD gave the [AMD Compilers for AMD Instinct™ Accelerators](https://www.youtube.com/watch?v=om8mjZ9yyws&t=143s) talk to explain the toolchains that it provides for its CPUs and GPUs. It also covers the MI300A handling in their OpenMP offloading capable compiler.

<a id="notions-of-debugging"></a>

### Notions of debugging

“At first, the machines were really simple but not powerful. Then they got really powerful, but really mean.”

How you debug a code is quite situational. Having thorough logs or a useful coredump is rare.

**Note**

This is an opinionated remark but, GDB is most useful when used on coredumps. It becomes quite tedious (impractical) on large software with many software threads or multiple processes.

One should try to add the following Clang/GCC C/C++ flag `-g` or its equivalent in other languages or compilers. This flags does not slow down your program and does not impact the generated machine code. It will largely increase your executable size but the debug information will not reside in the program’s memory space.

Somme notes on the ELF file format are given by Greg Law in [Linux Debuginfo Formats](https://www.youtube.com/watch?v=l3h7F9za_pc). ELF is used to represent your binaries on a machine like Adastra.

<a id="debugging-methodology"></a>

#### Debugging methodology

Over-quoted Kernighan said *that debugging is twice as hard as writing a program in the first place*. And obviously, that is somewhat true and makes for the first point: do not try to be too smart when implementing, though, not less smart than you need to be. For instance, the Linux Kernel is **very simple locally**, it is indeed simple C code, but as a whole, it becomes a very complex machinery. Try to figure out what code complexity you really need to implement and try to use tools to help you maintain good code quality.

If you have good code, most bugs are trivial. Though not necessarily easy to find, they are easy to fix and often can be found using the second point: the ancestral `printf` and comment technic. It can often allow you to do a binary search (dichotomy) in your code. As this can achieve logarithmic complexity in bug research, it is quite good, but not as good as knowing your code and developing an *intuition*. Now, depending on the low-levelness of your work, `printf` could turn into `gdb`, `strace`, etc..

The third point is **intuition** which you develop for your code, but you also by knowing more about the environment, the context it executes in. Intuition is probably the best method but it is not systematic compared to the other two.

Assuming the three other points above did not succeeded, the bug left are hard bugs and hard bugs cannot be solved unless you know more about your platform or program (problem) which means you need either to learn more on the subject (develop intuition) and take time do dissect the bug (good luck with that), or you can get help by using tools or asking someone more knowledgeable on the subject.

**Note**

On GPUs, if you write in HIP, CUDA, OpenMP targets, Kokkos, Sycl etc. you will have access to the `printf` function inside kernels (except for OpenMP target and Fortran).

<a id="a-note-on-benchmarks"></a>

### A note on benchmarks

Be careful with benchmarks, they only show how something behaves out of its context (encompassing the OS, hardware, network/IO, system calls, etc.).

Now, assuming any software, if the design says that *something* is the best solution for what you are trying to do, by all means use it, do not rely on some random guy (or guru) that tells you it’s slower and that you should not use it. By all means, use it, profile, and if its fast enough, there you go.

By “*something* is the best solution for what you are trying to do”, understand that you should use the proper tool for the job. Don’t use a sparse solver for a dense system, don’t use inheritance if you don’t need a customization point.

<a id="the-bash-unix-shell"></a>

<a id="learn-bash"></a>

### The Bash Unix shell

The basics to using the [Bash shell programming in Linux](https://arachnoid.com/linux/shell_programming.html).

<a id="on-the-issues-encountered-in-software-engineering"></a>

### On the issues encountered in software engineering

A celebrated classic is Fred Brooks’ The Mythical Man-Month, [ISBN-10: 0201835959](https://isbnsearch.org/isbn/9780201835953). It covers many aspect of complex software development. It is arranged in multiple real stories to motivate the points. While written a some 50 years ago, it will nonetheless consolidate your foundational understanding of software and how it is conceived.

<a id="network-programming-distributed-and-shared-memory-abstractions"></a>

### Network programming, distributed and shared memory abstractions

<a id="low-level-network-communication-concepts"></a>

#### Low level network communication concepts

[Details on the challenges and tradeoffs made when designing a library such as OpenFabric Interfaces](https://github.com/ofiwg/ofi-guide/blob/master/OFIGuide.md). This is a good all rounder document to anyone seeking to better understand how the lower level layer of an MPI implementation works. On the history of libfabric we have [A Brief Introduction to OpenFabrics (libfabric)](https://youtu.be/VApk4lkXsDg?t=339) by Sean Hefty.

Steve Scott presents [The Cray Shasta Architecture](https://www.youtube.com/watch?v=3J4mNasiiDo&t=359s), and notably the interconnect part, SlingShot. The roots of SlingShot are presented in [Cray High Speed Networking](https://www.youtube.com/watch?v=Tup1L_unHzM). Details on SlingShot are given in [An In-Depth Analysis of the Slingshot Interconnect](https://arxiv.org/pdf/2008.08886).

SlingShot and Ultra Ethernet (UE) are close as presented by Keith Underwood in [From SlingShot to Ultra Ethernet: Building a transport standard for libfabric](https://www.youtube.com/watch?v=3gpIx2ijvhU).

<a id="the-mpi-standard"></a>

#### The MPI standard

One should try to stick close to the standard and avoid relying on implementation specific behaviors. You can find the standard document for MPI 4.0 at this URL: [`https://www.mpi-forum.org/docs/mpi-4.0/mpi40-report.pdf`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/88f1bf8667a220281ea3acf27b69d239/mpi40-report.pdf) (retro compatible with previous standards).

A lighter explanation of the API can be found here: <https://www.mpich.org/static/docs/v4.0/>.

On Adastra you should use [Cray MPICH](../software_stack/libraries/index.md#adastra-software-stack-libraries-mpi-cray-mpich).

<a id="guidelines"></a>

##### Guidelines

- check your MPI affinity: NIC to GPU, rank/core to NIC, rank/core to GPU;
- do not mistake time spent in MPI and load imbalance ([HPCToolkit](../software_stack/tools/index.md#adastra-software-stack-tools-profiling-hpctoolkit) can be used to check for load imbalance);
  :   - some time imbalance comes comes from *noise*, as in jitter caused by external sources, say the OS.

- ask yourself, are you message rate or bandwidth bound ?
- post `irecv` first, do some work or even barrier, then do `isend`, do some work and then `waitall`;
  :   - on Cassini NICs (the one on Adastra) you can count the number of directly matched recv with the `LPE_NET_MATCH_PRIORITY` Cassini hardware counter and the non directly matched count with `LPE_NET_MATCH_OVERFLOW`.

- do not use too many communicators (<= 256);
- do not use too large tags (<= 65k), you can get the upper bound using `MPI_Comm_get_attr(comm, MPI_TAG_UB, &val, &flag)`;
- do not post an absurd number of immediate send/recv, say, less than 128 per rank at a given time;
- give MPI a chance to make progress (that is, process your `isend` / `irecv`, handle buffer copies, allocation, acknowledgment, etc.). You can call `MPI_Test` / `MPI_Wait` (and variants), but `MPI_TestSome` is better though (see Advice to users, page 81, MPI 4.0 standard) and with MPI 4.1, `MPI_Request_get_status` may be better;

<a id="gpuccl"></a>

#### GPUCCL

NCCL and RCCL are Collective Collection Libraries (CCL) that also provide basic send/receive operation. Their practical goal mostly revolves around providing higher collective network throughput at smaller buffer size compared to MPI (lowering collective latency at smaller buffer sizes). The often mentioned stream friendliness of CCL compared to MPI is indeed a practical advantage, but not a theoretical one; indeed, we could implement most of the CCL stream support on MPI using `[cuda|hip]StreamAddCallback`.

The landscape of GPU Centric communication is quite large and [this introduction](https://www.youtube.com/watch?v=IOtqqHAofmA) can help navigate it.

<a id="choosing-a-license"></a>

### Choosing a license

We are aware that researcher may not be interested or feel concerned about the licensing of their software. Only scratching the surface of the legal aspects of software and its use for computing, we would strongly advise the developers of a code to carefully choose a license for their code.

A high level breakdown of the most common licenses is given on [choosealicense.com](https://choosealicense.com/licenses/).

In France, there is also the [CeCCIL](http://www.cecill.info/) license which originated from CEA, CNRS and INRIA.

<a id="hardware-for-hpc"></a>

## Hardware for HPC

<a id="fast-forward-program"></a>

### Fast forward program

As is described is [`this 2015 SNL document`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/4fd84d7ff29cb5453837150acaabdfa2/snl_doe_forward.pdf), large HPC center or states with HPC interest must influence industry if they are to expect any kind of decent HPC hardware. All in all, they mostly succeeded (with AMD) following this plan:

- We need industry involvement:
  :   - Avoid one-off, stove-piped solutions;
      - Continued “product” availability and upgrades beyond DOE support.
- Industry cannot and will not solve the problem alone:
  :   - Business model obligates industry to optimize for profit, beat competitors;
      - Industry investments heavily weighted towards near-term, evolutionary improvements with small margin over competitors;
      - Industry funding for long-term technology R&D is limited and constrained;
      - Industry does not understand DOE Applications and Algorithms.
- How can we impact industry?
  :   - Work with those that have strong advocate(s) within the company;
      - Fund research, development and demonstration of long-term technologies that clearly show potential as future mass-market products (or product components);
      - Corollary: do not fund product development (as part of DOE R&D portfolio);
      - Industry will incorporate promising technologies into future product lines.

Other document on the subject include [`AMD's review of its Exascale plan`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/caba01424961713af89dedbfcad487bc/isca2023_exascale.pdf).

<a id="large-gpu-die-issues"></a>

### Large GPU die issues

Cerebras is a company that make very large AI chips. In [this video](https://www.youtube.com/watch?v=7GV_OdqzmIU), they explain the issue Nvidia has with scaling the production of their B200 chips (for the H200). AMD probably has had the same issue with their MI300A which are monstrous in size, both in width but also in height as modern chips are 3D, that is stacked silicon substrates and organic (PCB) layers placed on top of each other. The different Coefficient of Thermal Expansion (CTE) leads to complex design decisions.

<a id="mi300a"></a>

### MI300A

AMD engineers [`talk about how they produced the MI300A`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/484384c0c918544deb72dfe528d6affa/2024-isca-MI300A-exascale.pdf).

<a id="other"></a>

## Other

<a id="similar-hpc-systems-documentation"></a>

### Similar HPC systems’ documentation

- [LUMI documentation](https://docs.lumi-supercomputer.eu/);
- [OLCF training archive](https://docs.olcf.ornl.gov/training/training_archive.html).

<a id="standards"></a>

### Standards

- [`CDNA 2 ISA specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/6aee6a8038bd6881a42e8d29cf9d4046/instinct-mi200-cdna2-instruction-set-architecture.pdf);
- [`CDNA 3 ISA specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/0ccf34880584256c62e2dce65c9ba8b8/amd-instinct-mi300-cdna3-instruction-set-architecture.pdf);
- [`The C language 99 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/6c3e9974669446310395ddc4305e8830/C_1999_n1256.pdf);
- [`The C language 11 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/2ed5e18814beab7b64f7394b7a9ad174/C_2011_n1570.pdf);
- [`The C language 17 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/3cc4de612f6ecd36c3c56e5758ecf6f4/C_2017_n2310.pdf);
- [`The C++ language 11 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/7301418067098d784946b0b88bc5d61a/CPP_2011_n3242.pdf);
- [`The C++ language 14 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/9b2b72029fcdbf7a71eb281dc2059277/CPP_2014_n3797.pdf);
- [`The C++ language 17 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/ff370440f111a21d6c1e44de2fdcfff4/CPP_2017_n4640.pdf);
- [`The C++ language 20 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/4add578c004cbe87147fd72113fd37f1/CPP_2020_n4842.pdf);
- [`The Fortran language 90 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/d71d290d95981518849d1fe0af873e19/Fortran_1990_N692.pdf);
- [`The Fortran language 03 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/91b30eb00b39f6896fae528e5d0d66fc/Fortran_2003_N1601.pdf);
- [`The Fortran language 08 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/54a34648eb89751eded0bb162d4c1cc4/Fortran_2008_N1830.pdf);
- [`The Fortran language 23 specification draft`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/0cf89b7235ce863aefc03372d1591df0/Fortran_2023_draft.pdf);
- [`OpenMP 4.5 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/e7240ba79df7fe7843251c2a8379e741/OpenMP-API-Specification-4-5.pdf);
- [`OpenMP 5.1 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/b50cdea99af31163fb5deb2bebafbde1/OpenMP-API-Specification-5-1.pdf);
- [`OpenMP 5.2 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/99dfed6771563a2cddd31a9645bf9cf5/OpenMP-API-Specification-5-2.pdf);
- [`OpenMP 5 example`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/1ed61e5baf6c542d3b1672efce282939/openmp-examples-5-0-1.pdf);
- [`OpenACC 2.7 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/7086860017e48ed2c62daac741f9aa66/OpenACC.2.7.pdf);
- [`OpenCL C specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/15a2b71c5cf16af72253c800c1f86c56/OpenCL_API.pdf);
- [`The MPI 4.0 specification`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/88f1bf8667a220281ea3acf27b69d239/mpi40-report.pdf).

<a id="quantic"></a>

### Quantic

[`Quantic road map 2022 commissioned by the French government`](https://dci.dci-gitlab.cines.fr/webextranet/_downloads/f77e5a5d8d445a6d5cb003ea98855ebe/Feuille-de-route-QUANTIQUE-2022.pdf).
