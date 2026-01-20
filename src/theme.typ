#import "logic.typ": *
#import "toolbox.typ": *

// Gradients
#let sunset-gradient = gradient.linear(
  color.hsl(32deg, 74%, 60%),
  color.hsl(13deg, 95%, 50%),
)

#let sunset-gradient-2 = gradient.linear(
  color.hsl(32deg, 74%, 60%).transparentize(90%),
  color.hsl(13deg, 95%, 50%).transparentize(90%),
  relative: "parent",
)

#let sunset-gradient-3 = gradient.linear(
  color.hsl(32deg, 74%, 60%).transparentize(98%),
  color.hsl(13deg, 95%, 50%).transparentize(98%),
  relative: "parent",
)

#let black-gradient = gradient.linear(
  rgb("#000000").transparentize(90%),
  rgb("#000000").transparentize(20%),
  rgb("#000000").transparentize(10%),
  rgb("#000000").transparentize(10%),
  rgb("#000000").transparentize(10%),
)

// Styling Elements
#let bullet-color = color.hsl(13deg, 95%, 50%).transparentize(10%)
#let bullet() = {
  text(bullet-color)[#sym.circle.filled]
}

#let title(body) = {
  box(
    stroke: 6pt + sunset-gradient-3,
    inset: 0.0em,
  )[
    #box(stroke: 4pt + sunset-gradient-2, inset: 0.0em)[
      #box(stroke: 1pt + sunset-gradient, inset: 0.0em)[
        #box(
          stroke: 0.3pt + white.transparentize(50%),
          inset: 0.5em,
        )[
          #text(fill: sunset-gradient, weight: "bold")[
            #heading(level: 1, body)
          ]
        ]
      ]
    ]
  ]
}

// Slide Types
#let imgslide(title_txt, impath, caption) = {
  slide()[
    #title[#title_txt]
    #figure(image(impath, height: 80%, fit: "contain"), numbering: none, caption: [
      #set text(size: 10pt)
      #caption
    ])
  ]
}

#let indent(body) = (type: "indent", body: body)

#let list-slide(title-text, ..items) = slide[
  #title[#title-text]
  #set align(horizon)
  #set list(marker: bullet())

  #block(inset: 3em)[
    #one-by-one(
      ..items
        .pos()
        .map(item => {
          if type(item) == dictionary and item.at("type", default: none) == "indent" {
            pad(left: 1.5em, list(item.body))
          } else {
            list(item)
          }
        }),
    )
  ]
]

#let my-new-section(name, time) = slide[
  // 1. Define the formatted content for the list
  #let toc-entry = [
    #name
    #h(1fr)
    #text(size: 0.8em, weight: "regular")[#time]
  ]

  // 2. Register it
  #register-section(toc-entry)

  // 3. Page / Background setup
  #set page(margin: (x: 0em, y: 0em), background: image(
    "/assets/at-bg.jpg",
    width: 100%,
    height: 100%,
    fit: "cover",
  ))
  #place(top + left, box(fill: black-gradient, width: 100%, height: 100%))

  #box(height: 100%, clip: true)[
    // 4. Content
    #block(inset: (x: 2em, y: 1em))[
      #title[Agenda] // Or use your nested box design here if preferred
      #set text(fill: white)

      #side-by-side(gutter: 3mm, columns: (1.5fr, 2fr))[
        // Left column content (optional)
      ][
        #set align(horizon)
        #all-sections((sections, current) => {
          // 5. Map sections to apply fading logic
          let formatted-items = sections.map(section => {
            if section == current {
              // Highlight: Full opacity, bold
              text(weight: "bold", section)
            } else {
              // Inactive: Fade out
              text(fill: white.transparentize(70%), weight: "regular", section)
            }
          })

          // 6. Display the list
          enum(
            numbering: n => block(text(fill: sunset-gradient, weight: "bold", size: 25pt)[#n]),
            tight: false,
            body-indent: 2em,
            ..formatted-items,
          )
        })
      ]
    ]
  ]
]

#let title-slide(title_txt) = {
  slide[
    #set align(center + horizon)
    #title[#title_txt]
    #register-section[#title_txt]
  ]
}

#let inverted-image(path) = {
  // This logic applies a visual inversion filter
  set image(color-filter: c => c.negate())
  image(path)
}
